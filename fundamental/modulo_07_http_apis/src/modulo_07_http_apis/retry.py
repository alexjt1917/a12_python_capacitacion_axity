from __future__ import annotations

from datetime import UTC, datetime

import httpx


def compute_backoff_seconds(
    attempt: int, initial_delay: float = 0.5, factor: float = 2.0
) -> float:
    if attempt <= 0:
        raise ValueError("attempt debe ser mayor que 0")
    return round(initial_delay * (factor ** (attempt - 1)), 2)


def is_retryable_exception(error: Exception) -> bool:
    if isinstance(error, httpx.HTTPStatusError):
        status_code = error.response.status_code
        return status_code in {408, 425, 429, 500, 502, 503, 504}

    return isinstance(
        error,
        (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError),
    )


def now_utc_iso() -> str:
    return datetime.now(UTC).isoformat()
