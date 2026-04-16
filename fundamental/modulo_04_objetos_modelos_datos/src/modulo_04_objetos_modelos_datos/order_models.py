from __future__ import annotations

from dataclasses import dataclass, field
from functools import total_ordering
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


@total_ordering
@dataclass(frozen=True, slots=True)
class Order:
    order_id: int
    customer: str
    product: str
    quantity: int
    unit_price: float
    tax_rate: float = field(default=0.16)

    def __post_init__(self) -> None:
        if self.order_id <= 0:
            raise ValueError("order_id debe ser mayor que 0")
        if not self.customer.strip():
            raise ValueError("customer no puede estar vacío")
        if not self.product.strip():
            raise ValueError("product no puede estar vacío")
        if self.quantity <= 0:
            raise ValueError("quantity debe ser mayor que 0")
        if self.unit_price < 0:
            raise ValueError("unit_price no puede ser negativo")
        if not (0 <= self.tax_rate <= 1):
            raise ValueError("tax_rate debe estar entre 0 y 1")

    @property
    def subtotal(self) -> float:
        return round(self.quantity * self.unit_price, 2)

    @property
    def tax(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)

    def __str__(self) -> str:
        return (
            f"Order(id={self.order_id}, customer='{self.customer}', "
            f"product='{self.product}', total={self.total:.2f})"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.total == other.total

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.total < other.total

    @classmethod
    def from_pydantic(cls, data: "OrderIn") -> "Order":
        return cls(
            order_id=data.order_id,
            customer=data.customer,
            product=data.product,
            quantity=data.quantity,
            unit_price=data.unit_price,
            tax_rate=data.tax_rate,
        )


class OrderIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    order_id: int = Field(..., gt=0)
    customer: str = Field(..., min_length=1)
    product: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    tax_rate: float = Field(default=0.16, ge=0, le=1)

    @field_validator("customer", "product")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("no puede estar vacío")
        return value

    def to_entity(self) -> Order:
        return Order.from_pydantic(self)


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    customer: str
    product: str
    quantity: int
    unit_price: float
    tax_rate: float
    subtotal: float
    tax: float
    total: float

    @classmethod
    def from_entity(cls, order: Order) -> "OrderOut":
        return cls(
            order_id=order.order_id,
            customer=order.customer,
            product=order.product,
            quantity=order.quantity,
            unit_price=order.unit_price,
            tax_rate=order.tax_rate,
            subtotal=order.subtotal,
            tax=order.tax,
            total=order.total,
        )
