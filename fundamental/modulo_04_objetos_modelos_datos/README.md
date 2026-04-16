# Módulo 4 - Objetos y modelos de datos

## Objetivo
Modelar entidades con comportamientos y validaciones usando dataclasses y Pydantic.

## Componentes
- `Order`: entidad de dominio implementada como dataclass
- `OrderIn`: modelo de entrada validado con Pydantic
- `OrderOut`: modelo de salida serializable con Pydantic

## Funcionalidad
- Cálculo de `subtotal`, `tax` y `total`
- Comparación entre órdenes por total
- Conversión de `OrderIn` a `Order`
- Conversión de `Order` a `OrderOut`

## Ejecutar pruebas
```bash
poetry run pytest