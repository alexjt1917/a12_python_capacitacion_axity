from __future__ import annotations

import csv
import json
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path

from .models import SaleRecord


def read_sales_csv(csv_path: Path) -> list[SaleRecord]:
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {csv_path}")

    records: list[SaleRecord] = []

    with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            record = SaleRecord(
                order_id=int(row["order_id"]),
                customer=row["customer"].strip(),
                category=row["category"].strip(),
                quantity=int(row["quantity"]),
                unit_price=float(row["unit_price"]),
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
            )
            records.append(record)

    return records


def write_json(data: Mapping[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
