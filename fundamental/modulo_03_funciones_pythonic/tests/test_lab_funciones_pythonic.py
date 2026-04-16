from lab_funciones_pythonic import (
    construir_configuracion,
    crear_multiplicador,
    formatear_mensaje,
    generar_lotes,
    sumar_todos,
)


def test_formatear_mensaje():
    assert formatear_mensaje("Hola") == "[INFO] Hola"


def test_sumar_todos():
    assert sumar_todos(1, 2, 3) == 6


def test_construir_configuracion():
    config = construir_configuracion(debug=True, puerto=8080)
    assert config["debug"] is True
    assert config["puerto"] == 8080


def test_closure_multiplicador():
    duplicar = crear_multiplicador(2)
    assert duplicar(5) == 10


def test_generar_lotes():
    datos = [1, 2, 3, 4, 5]
    lotes = list(generar_lotes(datos, 2))
    assert lotes == [[1, 2], [3, 4], [5]]
