import matplotlib.pyplot as plt
from comparador import año_de_cruce

def grafica_costes(compra, alquiler, años):
    lista_años = []
    costes_compra = []
    costes_alquiler = []

    for año in range(1, años + 1):
        lista_años.append(año)
        costes_compra.append(compra.coste_total(año))
        costes_alquiler.append(alquiler.coste_total(año))

    plt.plot(lista_años, costes_compra, label="Comprar")
    plt.plot(lista_años, costes_alquiler, label="Alquilar")

    cruce = año_de_cruce(compra, alquiler)
    if cruce is not None:
        plt.axvline(cruce, color="gray", linestyle="--")
        plt.text(cruce, max(costes_alquiler) / 2, f" Compensa comprar desde el año {cruce}")

    plt.xlabel("Años")
    plt.ylabel("Coste acumulado (€)")
    plt.title("¿Comprar o alquilar?")
    plt.legend()
    plt.show()


def grafica_patrimonio(compra, años):
    plt.figure()
    lista_años = []
    valores = []
    deudas = []

    for año in range(0, años + 1):
        lista_años.append(año)
        valores.append(compra.valor_piso(año))
        deudas.append(compra.deuda(año))

    plt.plot(lista_años, valores, label="Valor del piso")
    plt.plot(lista_años, deudas, label="Deuda con el banco")
    plt.xlabel("Años")
    plt.ylabel("Euros (€)")
    plt.title("¿Cuánto es tuyo el piso?")
    plt.legend()
    plt.show()