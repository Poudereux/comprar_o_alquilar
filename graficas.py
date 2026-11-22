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