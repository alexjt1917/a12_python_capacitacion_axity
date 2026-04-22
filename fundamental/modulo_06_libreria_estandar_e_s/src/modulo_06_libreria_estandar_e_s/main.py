from __future__ import annotations

from pathlib import Path

from .io_utils import read_sales_csv, write_json
from .logger_config import configure_logger
from .metrics import calculate_sales_summary


def main() -> None:
    logger = configure_logger()

    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "data" / "input" / "sales.csv"
    output_path = project_root / "data" / "output" / "summary.json"

    logger.info("Iniciando proceso de ingesta de CSV")
    logger.info("Leyendo archivo de entrada: %s", input_path)

    try:
        records = read_sales_csv(input_path)
        logger.info("Se leyeron %s registros", len(records))

        summary = calculate_sales_summary(records)
        logger.info("Métricas calculadas correctamente")

        write_json(summary, output_path)
        logger.info("Resumen exportado a JSON en: %s", output_path)

    except FileNotFoundError as error:
        logger.error("Archivo no encontrado: %s", error)
        raise
    except ValueError as error:
        logger.error("Error de conversión de datos: %s", error)
        raise
    except Exception as error:
        logger.exception("Error inesperado durante la ejecución: %s", error)
        raise


if __name__ == "__main__":
    main()
