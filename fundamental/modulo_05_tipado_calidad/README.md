# Módulo 5 - Tipado estático opcional y calidad

## Objetivo
Extender el trabajo del módulo 4 para incorporar tipado estático, validación con mypy y automatización de calidad con ruff, black, isort, pre-commit y CI.

## Componentes
- `order_models.py`: entidad `Order` y modelos Pydantic tipados
- `typing_examples.py`: ejemplos de `Literal`, `TypedDict`, `Protocol` y unión `int | str`
- `tests/`: pruebas unitarias del dominio y de ejemplos de tipado

## Funcionalidad
- Cálculo de `subtotal`, `tax` y `total`
- Comparación entre órdenes por total
- Conversión de `OrderIn` a `Order`
- Conversión de `Order` a `OrderOut`
- Ejemplo de filtros tipados con `TypedDict`
- Estrategias de descuento con `Protocol`

## Ejecutar validaciones
```bash
poetry install
poetry run black .
poetry run isort .
poetry run ruff check .
poetry run mypy src tests
poetry run pytest
