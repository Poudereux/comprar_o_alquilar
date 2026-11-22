from entrada import pedir_numero
from opciones import Compra, Alquiler
from comparador import año_de_cruce
from graficas import grafica_costes, grafica_patrimonio


def crear_alquiler(compra):
    print("\n--- DATOS DEL ALQUILER ---")
    mensual = pedir_numero("Alquiler mensual (€): ")
    subida = pedir_numero("Subida anual del alquiler (%): ") / 100
    rentabilidad = pedir_numero("Rentabilidad si inviertes la entrada (%): ") / 100
    capital = compra.entrada + compra.precio * compra.gastos_compra
    return Alquiler(mensual, subida, capital, rentabilidad)


def crear_compra():
    print("\n--- DATOS DE LA COMPRA ---")
    precio = pedir_numero("Precio del piso (€): ")
    entrada = pedir_numero("Entrada (€): ")
    interes = pedir_numero("Interés de la hipoteca (%): ") / 100
    años = int(pedir_numero("Años de hipoteca: "))
    gastos_compra = pedir_numero("Gastos de compra (%): ") / 100
    gastos_anuales = pedir_numero("Gastos anuales: IBI, comunidad... (€): ")
    revalorizacion = pedir_numero("Revalorización anual del piso (%): ") / 100
    return Compra(precio, entrada, interes, años, gastos_compra, gastos_anuales, revalorizacion)


def mostrar_menu():
    print("\n===== ¿COMPRAR O ALQUILAR? =====")
    print("1. Introducir datos de la compra")
    print("2. Introducir datos del alquiler")
    print("3. Ver resultado")
    print("4. Gráfica: comprar vs alquilar")
    print("5. Gráfica: valor del piso vs deuda")
    print("6. Salir")


def main():
    compra = None
    alquiler = None

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            compra = crear_compra()
        elif opcion == "2":
            if compra is None:
                print("Primero introduce los datos de la compra (opción 1)")
            else:
                alquiler = crear_alquiler(compra)
        elif opcion == "3":
            if compra is None or alquiler is None:
                print("Primero introduce los datos de la compra y del alquiler (opciones 1 y 2)")
            else:
                cruce = año_de_cruce(compra, alquiler)
                if cruce is None:
                    print("Con estos datos, en 40 años nunca compensa comprar")
                else:
                    print(f"Comprar compensa a partir del año {cruce}")
        elif opcion == "4":
            if compra is None or alquiler is None:
                print("Primero introduce los datos (opciones 1 y 2)")
            else:
                grafica_costes(compra, alquiler, 30)
        elif opcion == "5":
            if compra is None:
                print("Primero introduce los datos de la compra (opción 1)")
            else:
                grafica_patrimonio(compra, 30)
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, elige del 1 al 6")


main()