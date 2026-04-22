from __future__ import annotations

from datetime import date

from modulo_06_libreria_estandar_e_s.metrics import calculate_sales_summary
from modulo_06_libreria_estandar_e_s.models import SaleRecord


def build_sample_records() -> list[SaleRecord]:
    return [
        SaleRecord(
            order_id=1,
            customer="Ana",
            category="tech",
            quantity=2,
            unit_price=150.0,
            date=date(2026, 4, 20),
        ),
        SaleRecord(
            order_id=2,
            customer="Luis",
            category="home",
            quantity=1,
            unit_price=300.0,
            date=date(2026, 4, 20),
        ),
    ]


def test_calculate_sales_summary() -> None:
    summary = calculate_sales_summary(build_sample_records())

    assert summary["total_orders"] == 2
    assert summary["total_revenue"] == 600.0
    assert summary["average_order_revenue"] == 300.0
    assert summary["max_order_revenue"] == 300.0
    assert summary["min_order_revenue"] == 300.0
    assert summary["revenue_by_category"] == {"home": 300.0, "tech": 300.0}


def test_calculate_sales_summary_empty() -> None:
    summary = calculate_sales_summary([])

    assert summary["total_orders"] == 0
    assert summary["total_revenue"] == 0.0
    assert summary["revenue_by_category"] == {}
