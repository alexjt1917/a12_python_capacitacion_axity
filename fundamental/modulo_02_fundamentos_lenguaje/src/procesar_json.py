import json
import re


def cargar_datos(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:
        print("Error: archivo no encontrado.")
        return []

    except json.JSONDecodeError:
        print("Error: formato JSON inválido.")
        return []


def filtrar_categoria(datos, categoria):
    return [item for item in datos if item["categoria"] == categoria]


def calcular_total(datos):
    return sum(item["precio"] * item["cantidad"] for item in datos)


def obtener_categorias_unicas(datos):
    return {item["categoria"] for item in datos}


def obtener_resumen(datos):
    total = calcular_total(datos)
    cantidad_items = len(datos)

    return total, cantidad_items


def validar_nombre_producto(nombre):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$"
    return bool(re.match(patron, nombre))


def menu():
    print("\nSeleccione categoría:")
    print("1. Tecnologia")
    print("2. Oficina")
    print("3. Todas")


def procesar_opcion(opcion, datos):
    match opcion:
        case "1":
            return filtrar_categoria(datos, "Tecnologia")

        case "2":
            return filtrar_categoria(datos, "Oficina")

        case "3":
            return datos

        case _:
            print("Opción inválida.")
            return []


def main():
    datos = cargar_datos("data/ventas.json")

    if not datos:
        return

    continuar = True

    while continuar:
        menu()
        opcion = input("Ingrese opción: ")

        datos_filtrados = procesar_opcion(opcion, datos)

        if datos_filtrados:
            total, cantidad = obtener_resumen(datos_filtrados)

            print("\nResultados:")
            for item in datos_filtrados:
                nombre = item["producto"]

                if validar_nombre_producto(nombre):
                    print(item)

            print(f"\nTotal: ${total}")
            print(f"Cantidad de registros: {cantidad}")

            categorias = obtener_categorias_unicas(datos)
            print(f"Categorías únicas: {categorias}")

        respuesta = input("\n¿Desea continuar? (s/n): ")

        if respuesta.lower() != "s":
            continuar = False


if __name__ == "__main__":
    main()
