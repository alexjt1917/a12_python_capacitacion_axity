from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from .models import SaleRecord


def calculate_sales_summary(records: list[SaleRecord]) -> dict[str, object]:
    if not records:
        return {
            "total_orders": 0,
            "total_revenue": 0.0,
            "average_order_revenue": 0.0,
            "max_order_revenue": 0.0,
            "min_order_revenue": 0.0,
            "revenue_by_category": {},
            "generated_at": datetime.now(UTC).isoformat(),
        }

    revenues = [record.revenue for record in records]
    revenue_by_category: defaultdict[str, float] = defaultdict(float)

    for record in records:
        revenue_by_category[record.category] += record.revenue

    return {
        "total_orders": len(records),
        "total_revenue": round(sum(revenues), 2),
        "average_order_revenue": round(sum(revenues) / len(revenues), 2),
        "max_order_revenue": round(max(revenues), 2),
        "min_order_revenue": round(min(revenues), 2),
        "revenue_by_category": {
            key: round(value, 2) for key, value in sorted(revenue_by_category.items())
        },
        "generated_at": datetime.now(UTC).isoformat(),
    }
