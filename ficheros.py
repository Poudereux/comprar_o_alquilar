from opciones import Compra, Alquiler

ARCHIVO = "escenarios.csv"


def guardar_escenario(nombre, compra, alquiler):
    datos = [nombre, compra.precio, compra.entrada, compra.interes_anual, compra.años,
             compra.gastos_compra, compra.gastos_anuales, compra.revalorizacion,
             alquiler.alquiler_mensual, alquiler.subida_anual, alquiler.rentabilidad]
    linea = ";".join(str(d) for d in datos)
    with open(ARCHIVO, "a", encoding="utf-8") as f:
        f.write(linea + "\n")


def cargar_escenarios():
    escenarios = {}
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split(";")
                compra = Compra(float(p[1]), float(p[2]), float(p[3]), int(p[4]),
                                float(p[5]), float(p[6]), float(p[7]))
                capital = compra.entrada + compra.precio * compra.gastos_compra
                alquiler = Alquiler(float(p[8]), float(p[9]), capital, float(p[10]))
                escenarios[p[0]] = (compra, alquiler)
    except FileNotFoundError:
        print("Todavía no hay escenarios guardados")
    return escenarios