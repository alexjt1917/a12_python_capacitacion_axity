from __future__ import annotations

from typing import Literal, Protocol, TypedDict

from .order_models import Order

OrderIdentifier = int | str
SalesChannel = Literal["web", "store", "phone"]


class OrderFilters(TypedDict, total=False):
    customer: str
    status: Literal["draft", "confirmed", "paid", "cancelled"]
    min_total: float
    channel: SalesChannel


class DiscountStrategy(Protocol):
    def apply(self, order: Order) -> float: ...


class NoDiscount:
    def apply(self, order: Order) -> float:
        return order.total


class PercentageDiscount:
    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 1:
            raise ValueError("percentage debe estar entre 0 y 1")
        self.percentage = percentage

    def apply(self, order: Order) -> float:
        return round(order.total * (1 - self.percentage), 2)


def find_order(order_id: OrderIdentifier, orders: list[Order]) -> Order | None:
    normalized_id = str(order_id)

    for order in orders:
        if str(order.order_id) == normalized_id:
            return order

    return None


def filter_orders(orders: list[Order], filters: OrderFilters) -> list[Order]:
    result = orders

    if "customer" in filters:
        result = [order for order in result if order.customer == filters["customer"]]

    if "status" in filters:
        result = [order for order in result if order.status == filters["status"]]

    if "min_total" in filters:
        result = [order for order in result if order.total >= filters["min_total"]]

    return result


def calculate_final_total(
    order: Order, strategy: DiscountStrategy | None = None
) -> float:
    if strategy is None:
        return order.total
    return strategy.apply(order)
