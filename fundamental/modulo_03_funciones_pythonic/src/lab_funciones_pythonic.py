import random
import time
from contextlib import contextmanager
from functools import wraps


def formatear_mensaje(mensaje, prefijo="INFO", sufijo=""):
    return f"[{prefijo}] {mensaje} {sufijo}".strip()


def sumar_todos(*args):
    return sum(args)


def construir_configuracion(**kwargs):
    return kwargs


def aplicar_operacion(datos, funcion):
    return [funcion(x) for x in datos]


def crear_multiplicador(factor):
    def multiplicar(numero):
        return numero * factor

    return multiplicar


def retry(
    max_intentos=3, delay_inicial=0.5, factor_backoff=2, excepciones=(Exception,)
):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = delay_inicial
            ultimo_error = None

            for intento in range(1, max_intentos + 1):
                try:
                    print(f"Intento {intento} de {max_intentos}")
                    return func(*args, **kwargs)
                except excepciones as error:
                    ultimo_error = error
                    print(f"Error detectado: {error}")

                    if intento < max_intentos:
                        print(f"Esperando {delay:.2f} segundos antes de reintentar...")
                        time.sleep(delay)
                        delay *= factor_backoff

            raise ultimo_error

        return wrapper

    return decorador


@contextmanager
def temporizador(nombre_bloque="bloque"):
    inicio = time.perf_counter()
    print(f"Iniciando temporización de: {nombre_bloque}")
    try:
        yield
    finally:
        fin = time.perf_counter()
        print(f"Tiempo de ejecución de {nombre_bloque}: {fin - inicio:.4f} segundos")


def generar_lotes(iterable, tamano_lote):
    lote = []

    for elemento in iterable:
        lote.append(elemento)
        if len(lote) == tamano_lote:
            yield lote
            lote = []

    if lote:
        yield lote


@retry(max_intentos=4, delay_inicial=0.2, factor_backoff=2, excepciones=(ValueError,))
def operacion_inestable(probabilidad_fallo=0.7):
    if random.random() < probabilidad_fallo:
        raise ValueError("Fallo aleatorio simulado.")

    return "Operación completada correctamente"


def main():
    print("\n--- Funciones y argumentos ---")
    print(formatear_mensaje("Hola mundo"))
    print(formatear_mensaje("Proceso completado", prefijo="OK", sufijo="✓"))
    print("Suma con *args:", sumar_todos(1, 2, 3, 4, 5))
    print(
        "Configuración con **kwargs:",
        construir_configuracion(host="localhost", puerto=8080, debug=True),
    )

    print("\n--- Lambda y comprensión ---")
    numeros = [1, 2, 3, 4, 5]
    cuadrados = aplicar_operacion(numeros, lambda x: x**2)
    print("Números:", numeros)
    print("Cuadrados:", cuadrados)

    print("\n--- Closure ---")
    duplicar = crear_multiplicador(2)
    triplicar = crear_multiplicador(3)
    print("Duplicar 10:", duplicar(10))
    print("Triplicar 10:", triplicar(10))

    print("\n--- Generador por lotes ---")
    datos = list(range(1, 11))
    for indice, lote in enumerate(generar_lotes(datos, 3), start=1):
        print(f"Lote {indice}: {lote}")

    print("\n--- Context manager de temporización ---")
    with temporizador("procesamiento de lotes"):
        total = sum(x for x in range(100000))
        print("Total calculado:", total)

    print("\n--- Decorador de reintentos con backoff ---")
    try:
        resultado = operacion_inestable()
        print(resultado)
    except ValueError as error:
        print(f"La operación falló definitivamente: {error}")


if __name__ == "__main__":
    main()
