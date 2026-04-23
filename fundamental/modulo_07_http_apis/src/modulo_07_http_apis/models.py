from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DownloadConfig:
    url: str
    output_path: Path
    timeout_seconds: float = 10.0
    max_attempts: int = 3
    chunk_size: int = 8192
    initial_delay: float = 0.5
    backoff_factor: float = 2.0
