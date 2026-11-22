import matplotlib.pyplot as plt

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
    plt.xlabel("Años")
    plt.ylabel("Coste acumulado (€)")
    plt.title("¿Comprar o alquilar?")
    plt.legend()
    plt.show()