# Módulo 7 - HTTP y consumo de APIs

## Objetivo
Construir un cliente HTTP robusto con `httpx`, configurando timeouts, reintentos y descarga por streaming a disco.

## Conceptos aplicados
- `httpx` para cliente HTTP síncrono
- timeouts configurables
- reintentos con backoff
- manejo de errores HTTP y de red
- descarga por streaming para uso eficiente de memoria
- `logging` para observabilidad del proceso

## Flujo del laboratorio
1. Crear configuración de descarga
2. Ejecutar petición HTTP con timeout
3. Reintentar ante errores transitorios
4. Descargar respuesta por streaming
5. Guardar archivo en disco
6. Registrar eventos con logging

## Ejecutar pruebas

```bash
poetry run pytest