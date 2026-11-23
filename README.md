# ¿Comprar o alquilar una vivienda en Madrid?

Proyecto de Programación I — Grado en Análisis de Datos y Negocios (UFV)
Autor: Miguel Poudereux

## La pregunta

Si vivo en Madrid, ¿me compensa más comprar un piso con hipoteca o vivir de alquiler? Y si compensa comprar, **¿a partir de qué año?**

El programa compara las dos opciones año a año y calcula cuánto cuesta realmente cada una: no solo lo que pagas, sino también lo que ganas (el piso que es tuyo, o el dinero que inviertes si no compras).

## La respuesta

Con datos actuales de Madrid capital para un piso de 70 m², **comprar compensa a partir del año 3**.

El motivo principal es que ahora mismo el alquiler (unos 1.638 €/mes) es más caro que la cuota de la hipoteca (unos 1.528 €/mes), y además el piso va ganando valor.

Pero la respuesta depende mucho de las hipótesis. El programa permite probar escenarios:

| Si el piso sube al año… | …y el dinero invertido rinde | Compensa comprar desde |
|---|---|---|
| 2,5 % | 4 % | año 3 |
| 0 % | 4 % | año 9 |
| 0 % | 6 % | año 18 |
| −1 % | 5 % | año 21 |

**Conclusión:** comprar sale mejor si piensas quedarte varios años en el piso y su precio no baja. Si el piso no se revaloriza y el dinero de la entrada se puede invertir bien, alquilar compensa durante mucho más tiempo.

## Cómo se calcula

**Coste de comprar** después de X años:

```
entrada + gastos de compra + cuotas pagadas + gastos anuales − (valor del piso − deuda pendiente)
```

**Coste de alquilar** después de X años:

```
rentas pagadas − lo que ha ganado el dinero de la entrada invertido
```

El programa busca el **primer año en que comprar cuesta menos que alquilar**.

## Estructura del proyecto

| Archivo | Qué hace |
|---|---|
| `finanzas.py` | Fórmulas de la hipoteca: cuota mensual y deuda pendiente |
| `opciones.py` | Clases `Compra` y `Alquiler`. Las dos tienen el método `coste_total(años)` (polimorfismo) |
| `comparador.py` | Función `año_de_cruce`, que responde a la pregunta |
| `graficas.py` | Gráfica de costes (compra vs alquiler) y gráfica de patrimonio (valor del piso vs deuda) |
| `entrada.py` | Pide números al usuario y controla errores con `try / except` |
| `ficheros.py` | Guarda y carga escenarios en `escenarios.csv` |
| `main.py` | Menú principal del programa |
| `pruebas.py` | Comprobaciones de cada parte con resultados conocidos |
| `app.py` | Web interactiva con Streamlit. Usa las mismas clases y funciones que `main.py` |

Conceptos de la asignatura que se usan: funciones, bucles `for` y `while`, condicionales, listas, diccionarios, clases y objetos, polimorfismo, excepciones, ficheros CSV, módulos, entorno virtual y Git.

## Cómo ejecutarlo

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

En Mac, usar `python3` y `source .venv/bin/activate`.

**Web interactiva** (mismos cálculos, con deslizadores y gráficas en el navegador):

```
streamlit run app.py
```

Menú:

1. Introducir datos de la compra
2. Introducir datos del alquiler
3. Ver resultado
4. Gráfica: comprar vs alquilar
5. Gráfica: valor del piso vs deuda
6. Guardar escenario
7. Cargar escenario
8. Salir

## Diagramas de flujo

![Función año_de_cruce](docs/diagrama_1_ano_de_cruce.png)

![Programa principal](docs/diagrama_2_programa_principal.png)

## Datos utilizados

Piso de 70 m² en Madrid capital.

**Compra**

| Dato | Valor | Fuente |
|---|---|---|
| Precio | 453.000 € | 70 m² × 6.471 €/m² (Idealista, agosto 2026) |
| Entrada | 90.600 € | 20 % del precio, lo habitual que piden los bancos |
| Interés de la hipoteca | 3 % | Media de hipotecas a tipo fijo: 3,03 % (INE, julio 2026) |
| Plazo | 30 años | Plazo habitual |
| Gastos de compra | 8 % | ITP del 6 % en Madrid más notaría y registro |
| Gastos anuales | 2.000 € | Estimación de IBI, comunidad y seguro |
| Revalorización | 2,5 % al año | Hipótesis a largo plazo |

**Alquiler**

| Dato | Valor | Fuente |
|---|---|---|
| Alquiler mensual | 1.638 € | 70 m² × 23,4 €/m² (Idealista, octubre 2026) |
| Subida anual | 3 % | Hipótesis a largo plazo (ahora sube un 7,7 %, pero no es sostenible 30 años) |
| Rentabilidad de invertir la entrada | 4 % | Hipótesis |

## Limitaciones

- Las subidas de precios y alquileres a 30 años son **hipótesis**: nadie sabe cómo evolucionará el mercado.
- El interés de la hipoteca se considera fijo durante toda la vida del préstamo.
- No se tienen en cuenta deducciones fiscales, derramas, reformas ni la inflación.
- Si alquilas, solo se invierte el dinero de la entrada, no la diferencia mensual entre alquiler y cuota.

## Uso de IA

Siguiendo las normas de la asignatura, indico cómo he usado la IA (Claude):

- Para que me explicara los conceptos que no entendía (funciones, clases, bucles, excepciones, ficheros), con ejemplos distintos a los del proyecto.
- Para que me guiara paso a paso en la estructura del proyecto y en la instalación (Python, entorno virtual, Git).
- Para ayudarme a entender y corregir los errores que me salían.
- Para darme partes del código cuando me quedaba bloqueado, que luego he escrito a mano, probado y entendido.
- Para buscar los datos reales de Madrid y sus fuentes, y para ayudarme a redactar este README.
- La web interactiva (`app.py`) y los diagramas de flujo los ha generado la IA a partir de mis clases y funciones.

Todo el código lo he escrito y ejecutado yo en VS Code, y he comprobado cada parte con `pruebas.py`.