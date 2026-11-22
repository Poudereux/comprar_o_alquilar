def año_de_cruce(compra, alquiler):
    for año in range(1, 41):
        if compra.coste_total(año) < alquiler.coste_total(año):
            return año
    return None