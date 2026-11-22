from finanzas import cuota_mensual, deuda_pendiente

class Compra:
    def __init__(self, precio, entrada, interes_anual, años, gastos_compra, gastos_anuales, revalorizacion):
        self.precio = precio
        self.entrada = entrada
        self.interes_anual = interes_anual
        self.años = años
        self.gastos_compra = gastos_compra
        self.gastos_anuales = gastos_anuales
        self.revalorizacion = revalorizacion

    def cuota(self):
        capital = self.precio - self.entrada
        return cuota_mensual(capital, self.interes_anual, self.años)

    def valor_piso(self, años):
        return self.precio * (1 + self.revalorizacion) ** años

    def deuda(self, años):
        capital = self.precio - self.entrada
        meses = min(años * 12, self.años * 12)
        return deuda_pendiente(capital, self.interes_anual, self.años, meses)
    def coste_total(self, años):
        meses = min(años * 12, self.años * 12)
        pagado = self.entrada + self.precio * self.gastos_compra + self.cuota() * meses + self.gastos_anuales * años
        patrimonio = self.valor_piso(años) - self.deuda(años)
        return pagado - patrimonio

class Alquiler:
    def __init__(self, alquiler_mensual, subida_anual, capital_invertido, rentabilidad):
        self.alquiler_mensual = alquiler_mensual
        self.subida_anual = subida_anual
        self.capital_invertido = capital_invertido
        self.rentabilidad = rentabilidad

    def renta_del_año(self, año):
        return self.alquiler_mensual * 12 * (1 + self.subida_anual) ** (año - 1)

    def ganancia_inversion(self, años):
        return self.capital_invertido * ((1 + self.rentabilidad) ** años - 1)

    def coste_total(self, años):
        total = 0
        for año in range(1, años + 1):
            total = total + self.renta_del_año(año)
        return total - self.ganancia_inversion(años)