from __future__ import annotations

import logging
import time
from collections.abc import Callable
from pathlib import Path

import httpx

from .exceptions import DownloadError
from .models import DownloadConfig
from .retry import compute_backoff_seconds, is_retryable_exception


def make_http_client(
    timeout_seconds: float, transport: httpx.BaseTransport | None = None
) -> httpx.Client:
    timeout = httpx.Timeout(timeout_seconds)
    return httpx.Client(
        timeout=timeout,
        follow_redirects=True,
        transport=transport,
    )


def stream_download(
    client: httpx.Client,
    url: str,
    output_path: Path,
    chunk_size: int,
    logger: logging.Logger,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with client.stream("GET", url) as response:
        response.raise_for_status()

        with output_path.open("wb") as file:
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)

    logger.info("Descarga completada en: %s", output_path)


def download_with_retry(
    config: DownloadConfig,
    transport: httpx.BaseTransport | None = None,
    sleep_func: Callable[[float], None] = time.sleep,
) -> Path:
    logger = logging.getLogger("modulo_07_http_apis")
    last_error: Exception | None = None

    with make_http_client(
        timeout_seconds=config.timeout_seconds,
        transport=transport,
    ) as client:
        for attempt in range(1, config.max_attempts + 1):
            try:
                logger.info("Intento %s de %s", attempt, config.max_attempts)
                stream_download(
                    client=client,
                    url=config.url,
                    output_path=config.output_path,
                    chunk_size=config.chunk_size,
                    logger=logger,
                )
                return config.output_path

            except httpx.HTTPStatusError as error:
                last_error = error

                if not is_retryable_exception(error) or attempt == config.max_attempts:
                    logger.error(
                        "Error HTTP no recuperable o sin intentos restantes: %s",
                        error,
                    )
                    raise DownloadError("La descarga falló por error HTTP") from error

                delay = compute_backoff_seconds(
                    attempt=attempt,
                    initial_delay=config.initial_delay,
                    factor=config.backoff_factor,
                )
                logger.warning(
                    "Error HTTP transitorio (%s). Reintentando en %s segundos...",
                    error.response.status_code,
                    delay,
                )
                sleep_func(delay)

            except (
                httpx.TimeoutException,
                httpx.NetworkError,
                httpx.RemoteProtocolError,
            ) as error:
                last_error = error

                if attempt == config.max_attempts:
                    logger.error("Se agotaron los intentos: %s", error)
                    raise DownloadError(
                        "La descarga falló tras varios intentos"
                    ) from error

                delay = compute_backoff_seconds(
                    attempt=attempt,
                    initial_delay=config.initial_delay,
                    factor=config.backoff_factor,
                )
                logger.warning(
                    "Error transitorio de red/timeout. Reintentando en %s segundos...",
                    delay,
                )
                sleep_func(delay)

    raise DownloadError("La descarga falló") from last_error
