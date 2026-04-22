from __future__ import annotations

from pathlib import Path

from modulo_06_libreria_estandar_e_s.io_utils import read_sales_csv, write_json


def test_read_sales_csv(tmp_path: Path) -> None:
    csv_file = tmp_path / "sales.csv"
    csv_file.write_text(
        "order_id,customer,category,quantity,unit_price,date\n"
        "1,Ana,tech,2,150.0,2026-04-20\n",
        encoding="utf-8",
    )

    records = read_sales_csv(csv_file)

    assert len(records) == 1
    assert records[0].customer == "Ana"
    assert records[0].revenue == 300.0


def test_write_json(tmp_path: Path) -> None:
    output_file = tmp_path / "output" / "summary.json"
    # payload = {"total_orders": 1, "total_revenue": 300.0} #antes
    payload: dict[str, object] = {"total_orders": 1, "total_revenue": 300.0}

    write_json(payload, output_file)

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8")
