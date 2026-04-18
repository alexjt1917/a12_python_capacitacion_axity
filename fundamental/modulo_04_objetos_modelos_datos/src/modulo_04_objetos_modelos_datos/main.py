from modulo_04_objetos_modelos_datos.order_models import OrderIn, OrderOut


def main() -> None:
    payload = {
        "order_id": 1,
        "customer": "Alejandro",
        "product": "Laptop",
        "quantity": 2,
        "unit_price": 10000.0,
        "tax_rate": 0.16,
    }

    print("=== Creando OrderIn ===")
    order_in = OrderIn(**payload)
    print(order_in)

    print("\n=== Convirtiendo a entidad (dataclass) ===")
    order = order_in.to_entity()
    print(order)

    print("\n=== Cálculos derivados ===")
    print("Subtotal:", order.subtotal)
    print("Tax:", order.tax)
    print("Total:", order.total)

    print("\n=== Convirtiendo a salida ===")
    order_out = OrderOut.from_entity(order)
    print(order_out.model_dump())

    print("\n=== JSON ===")
    print(order_out.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
