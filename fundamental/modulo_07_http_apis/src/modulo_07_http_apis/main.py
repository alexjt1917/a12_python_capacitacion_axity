from __future__ import annotations

from pathlib import Path

from .client import download_with_retry
from .logger_config import configure_logger
from .models import DownloadConfig


def main() -> None:
    logger = configure_logger()

    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "data" / "downloads" / "sample_bytes.bin"

    config = DownloadConfig(
        url="https://httpbin.org/bytes/2048",
        output_path=output_path,
        timeout_seconds=10.0,
        max_attempts=3,
        chunk_size=1024,
    )

    logger.info("Iniciando laboratorio de cliente HTTP con streaming")

    try:
        downloaded_path = download_with_retry(config)
        logger.info("Archivo descargado correctamente en: %s", downloaded_path)
    except Exception as error:
        logger.exception("Fallo en la ejecución del laboratorio: %s", error)
        raise


if __name__ == "__main__":
    main()
