def cuota_mensual(capital, interes_anual, años):
    i = interes_anual / 12
    n = años * 12
    cuota = capital * i / (1 - (1 + i) ** -n)
    return cuota

def deuda_pendiente(capital, interes_anual, años, meses_pagados):
    i = interes_anual / 12
    cuota = cuota_mensual(capital, interes_anual, años)
    deuda = capital * (1 + i) ** meses_pagados - cuota * ((1 + i) ** meses_pagados - 1) / i
    return deuda