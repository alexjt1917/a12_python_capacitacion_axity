from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from modulo_07_http_apis.client import download_with_retry
from modulo_07_http_apis.exceptions import DownloadError
from modulo_07_http_apis.models import DownloadConfig


def test_download_with_retry_success(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"abc123", request=request)

    transport = httpx.MockTransport(handler)
    output_path = tmp_path / "download.bin"

    config = DownloadConfig(
        url="https://example.com/file.bin",
        output_path=output_path,
        max_attempts=3,
    )

    result = download_with_retry(
        config=config,
        transport=transport,
        sleep_func=lambda _: None,
    )

    assert result.exists()
    assert result.read_bytes() == b"abc123"


def test_download_with_retry_retries_then_succeeds(tmp_path: Path) -> None:
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1

        if calls["count"] == 1:
            return httpx.Response(503, request=request)

        return httpx.Response(200, content=b"retry-ok", request=request)

    transport = httpx.MockTransport(handler)
    output_path = tmp_path / "retry.bin"

    config = DownloadConfig(
        url="https://example.com/retry.bin",
        output_path=output_path,
        max_attempts=3,
    )

    result = download_with_retry(
        config=config,
        transport=transport,
        sleep_func=lambda _: None,
    )

    assert calls["count"] == 2
    assert result.read_bytes() == b"retry-ok"


def test_download_with_retry_fails_on_non_retryable_error(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, request=request)

    transport = httpx.MockTransport(handler)
    output_path = tmp_path / "missing.bin"

    config = DownloadConfig(
        url="https://example.com/missing.bin",
        output_path=output_path,
        max_attempts=3,
    )

    with pytest.raises(DownloadError, match="La descarga falló por error HTTP"):
        download_with_retry(
            config=config,
            transport=transport,
            sleep_func=lambda _: None,
        )
