# Módulo 6 - Librería estándar y E/S

## Objetivo
Implementar un flujo de ingesta de CSV, cálculo de métricas y exportación a JSON usando librería estándar de Python.

## Conceptos aplicados
- `pathlib` para manejo seguro de rutas y archivos
- `csv` para lectura tabular
- `json` para serialización
- `datetime` para fechas y marca de tiempo de generación
- `logging` para mensajes estructurados con distintos niveles

## Flujo del laboratorio
1. Leer `sales.csv`
2. Convertir cada fila a una entidad `SaleRecord`
3. Calcular métricas agregadas
4. Exportar resultado a `summary.json`
5. Registrar el proceso con logging

## Ejecutar pruebas

```bash
poetry run pytest