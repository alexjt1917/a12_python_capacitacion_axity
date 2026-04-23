from __future__ import annotations

import httpx
import pytest

from modulo_07_http_apis.retry import compute_backoff_seconds, is_retryable_exception


def test_compute_backoff_seconds() -> None:
    assert compute_backoff_seconds(1) == 0.5
    assert compute_backoff_seconds(2) == 1.0
    assert compute_backoff_seconds(3) == 2.0


def test_compute_backoff_seconds_invalid_attempt() -> None:
    with pytest.raises(ValueError, match="attempt debe ser mayor que 0"):
        compute_backoff_seconds(0)


def test_is_retryable_exception_http_503() -> None:
    request = httpx.Request("GET", "https://example.com/file.bin")
    response = httpx.Response(503, request=request)
    error = httpx.HTTPStatusError(
        "Service unavailable", request=request, response=response
    )

    assert is_retryable_exception(error) is True


def test_is_retryable_exception_http_404() -> None:
    request = httpx.Request("GET", "https://example.com/file.bin")
    response = httpx.Response(404, request=request)
    error = httpx.HTTPStatusError("Not found", request=request, response=response)

    assert is_retryable_exception(error) is False
