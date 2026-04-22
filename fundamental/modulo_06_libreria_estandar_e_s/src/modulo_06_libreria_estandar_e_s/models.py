from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class SaleRecord:
    order_id: int
    customer: str
    category: str
    quantity: int
    unit_price: float
    date: date

    @property
    def revenue(self) -> float:
        return round(self.quantity * self.unit_price, 2)
