from modulo_05_tipado_calidad.order_models import Order
from modulo_05_tipado_calidad.typing_examples import (
    PercentageDiscount,
    calculate_final_total,
    filter_orders,
    find_order,
)


def build_sample_orders() -> list[Order]:
    return [
        Order(
            order_id=1,
            customer="Alex",
            product="Laptop",
            quantity=1,
            unit_price=10000.0,
            status="draft",
        ),
        Order(
            order_id=2,
            customer="Ana",
            product="Mouse",
            quantity=2,
            unit_price=500.0,
            status="paid",
        ),
    ]


def test_find_order_accepts_int_or_str() -> None:
    orders = build_sample_orders()

    assert find_order(1, orders) is not None
    assert find_order("2", orders) is not None
    assert find_order("999", orders) is None


def test_filter_orders_by_status() -> None:
    orders = build_sample_orders()

    paid_orders = filter_orders(orders, {"status": "paid"})

    assert len(paid_orders) == 1
    assert paid_orders[0].customer == "Ana"


def test_calculate_final_total_with_discount() -> None:
    order = Order(
        order_id=3,
        customer="Luis",
        product="Audífonos",
        quantity=1,
        unit_price=1000.0,
        tax_rate=0.16,
    )

    strategy = PercentageDiscount(0.10)
    final_total = calculate_final_total(order, strategy)

    assert final_total == 1044.0
