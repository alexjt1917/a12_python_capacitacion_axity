import pytest
from pydantic import ValidationError

from modulo_04_objetos_modelos_datos.order_models import Order, OrderIn, OrderOut


def test_order_calculated_properties() -> None:
    order = Order(
        order_id=1,
        customer="Alex",
        product="Mouse",
        quantity=2,
        unit_price=100.0,
        tax_rate=0.16,
    )

    assert order.subtotal == 200.0
    assert order.tax == 32.0
    assert order.total == 232.0


def test_order_comparison_by_total() -> None:
    order_small = Order(
        order_id=1,
        customer="Alex",
        product="Mouse",
        quantity=1,
        unit_price=100.0,
    )
    order_big = Order(
        order_id=2,
        customer="Alex",
        product="Monitor",
        quantity=2,
        unit_price=300.0,
    )

    assert order_small < order_big
    assert order_big > order_small
    assert order_small != order_big


def test_order_invalid_quantity() -> None:
    with pytest.raises(ValueError, match="quantity debe ser mayor que 0"):
        Order(
            order_id=1,
            customer="Alex",
            product="Mouse",
            quantity=0,
            unit_price=100.0,
        )


def test_order_in_validation_error() -> None:
    with pytest.raises(ValidationError):
        OrderIn(
            order_id=1,
            customer="Alex",
            product="Mouse",
            quantity=-1,
            unit_price=100.0,
        )


def test_order_in_to_entity() -> None:
    order_in = OrderIn(
        order_id=1,
        customer="Alex",
        product="Laptop",
        quantity=1,
        unit_price=10000.0,
        tax_rate=0.16,
    )

    order = order_in.to_entity()

    assert isinstance(order, Order)
    assert order.customer == "Alex"
    assert order.total == 11600.0


def test_order_out_from_entity() -> None:
    order = Order(
        order_id=10,
        customer="Alex",
        product="Laptop",
        quantity=1,
        unit_price=10000.0,
        tax_rate=0.16,
    )

    order_out = OrderOut.from_entity(order)

    assert order_out.order_id == 10
    assert order_out.subtotal == 10000.0
    assert order_out.tax == 1600.0
    assert order_out.total == 11600.0
