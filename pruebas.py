from finanzas import cuota_mensual, deuda_pendiente
from opciones import Compra, Alquiler
from comparador import año_de_cruce
from graficas import grafica_costes

print(f"La cuota es {cuota_mensual(150000, 0.04, 25):.2f} €")
print(f"Deuda pendiente: {deuda_pendiente(150000, 0.04, 25, 120):.2f} €")

piso = Compra(250000, 50000, 0.03, 30, 0.10, 1500, 0.02)
print(f"Cuota: {piso.cuota():.2f} €")
print(f"Valor del piso en 10 años: {piso.valor_piso(10):.2f} €")

alquiler = Alquiler(1000, 0.03)
print(f"Año 1: {alquiler.renta_del_año(1):.2f} €")
print(f"Año 2: {alquiler.renta_del_año(2):.2f} €")
print(f"Alquiler 2 años: {alquiler.coste_total(2):.2f} €")

print(f"Deuda en 10 años: {piso.deuda(10):.2f} €")
print(f"Deuda en 35 años: {piso.deuda(35):.2f} €")

print(f"Comprar 10 años: {piso.coste_total(10):.2f} €")
print(f"Alquilar 10 años: {alquiler.coste_total(10):.2f} €")

print(f"Comprar compensa a partir del año {año_de_cruce(piso, alquiler)}")

grafica_costes(piso, alquiler, 30)