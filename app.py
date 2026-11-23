"""
Web interactiva del proyecto: ¿Comprar o alquilar una vivienda en Madrid?

Usa las MISMAS clases y funciones que el programa de consola (main.py):
  - Compra y Alquiler (opciones.py)
  - año_de_cruce (comparador.py)
  - guardar_escenario y cargar_escenarios (ficheros.py)
Lo único nuevo es la interfaz gráfica, hecha con Streamlit.

Para ejecutarla:  streamlit run app.py
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from comparador import año_de_cruce
from ficheros import cargar_escenarios, guardar_escenario
from opciones import Alquiler, Compra

# ---------------------------------------------------------------------
# Configuración y estilo
# ---------------------------------------------------------------------
AZUL = "#1F3864"
NARANJA = "#E07B39"
VERDE = "#2E8B57"

st.set_page_config(page_title="¿Comprar o alquilar?", page_icon="🏠", layout="wide")

st.markdown(
    f"""
    <style>
    .respuesta {{
        background: {AZUL}; color: white; border-radius: 14px;
        padding: 22px 28px; margin: 6px 0 18px 0;
    }}
    .respuesta h2 {{ color: white; margin: 0 0 6px 0; font-size: 1.9rem; }}
    .respuesta p {{ margin: 0; opacity: 0.85; font-size: 1.05rem; }}
    div[data-testid="stMetricValue"] {{ font-size: 1.6rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Datos reales de Madrid (ver README): piso de 70 m²
DATOS_MADRID = {
    "precio": 453000.0,      # 70 m² × 6.471 €/m² (Idealista)
    "entrada": 90600.0,      # 20 % del precio
    "interes": 3.0,          # % hipoteca a tipo fijo (INE)
    "años": 30,
    "gastos_compra": 8.0,    # % ITP 6 % + notaría y registro
    "gastos_anuales": 2000.0,
    "revalorizacion": 2.5,   # % anual (hipótesis)
    "alquiler": 1638.0,      # 70 m² × 23,4 €/m² (Idealista)
    "subida": 3.0,           # % anual (hipótesis)
    "rentabilidad": 4.0,     # % anual (hipótesis)
}

# La primera vez que se abre la web, se cargan los datos de Madrid
for clave, valor in DATOS_MADRID.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


def euros(x):
    """Formatea un número como euros al estilo español: 1.234.567 €"""
    return f"{x:,.0f} €".replace(",", ".")


def restablecer_madrid():
    for clave, valor in DATOS_MADRID.items():
        st.session_state[clave] = valor


def aplicar_escenario(compra, alquiler):
    """Pasa un escenario cargado del CSV a los controles de la web."""
    st.session_state["precio"] = compra.precio
    st.session_state["entrada"] = compra.entrada
    st.session_state["interes"] = compra.interes_anual * 100
    st.session_state["años"] = compra.años
    st.session_state["gastos_compra"] = compra.gastos_compra * 100
    st.session_state["gastos_anuales"] = compra.gastos_anuales
    st.session_state["revalorizacion"] = compra.revalorizacion * 100
    st.session_state["alquiler"] = alquiler.alquiler_mensual
    st.session_state["subida"] = alquiler.subida_anual * 100
    st.session_state["rentabilidad"] = alquiler.rentabilidad * 100


def crear_objetos(precio, entrada, interes, años, gastos_compra, gastos_anuales,
                  revalorizacion, mensual, subida, rentabilidad):
    """Igual que crear_compra() y crear_alquiler() de main.py, pero con los datos de la web."""
    compra = Compra(precio, entrada, interes / 100, años, gastos_compra / 100,
                    gastos_anuales, revalorizacion / 100)
    capital = compra.entrada + compra.precio * compra.gastos_compra
    alquiler = Alquiler(mensual, subida / 100, capital, rentabilidad / 100)
    return compra, alquiler


# ---------------------------------------------------------------------
# Barra lateral: los datos (lo mismo que preguntan las opciones 1 y 2 del menú)
# ---------------------------------------------------------------------
with st.sidebar:
    st.header("🏠 Compra")
    st.number_input("Precio del piso (€)", min_value=10000.0, step=5000.0, format="%.0f", key="precio")
    st.number_input("Entrada (€)", min_value=0.0, step=1000.0, format="%.0f", key="entrada")
    st.slider("Interés de la hipoteca (%)", 0.5, 7.0, step=0.05, key="interes")
    st.slider("Años de hipoteca", 5, 40, key="años")
    st.slider("Gastos de compra (%)", 0.0, 15.0, step=0.5, key="gastos_compra")
    st.number_input("Gastos anuales: IBI, comunidad... (€)", min_value=0.0, step=100.0,
                    format="%.0f", key="gastos_anuales")
    st.slider("Revalorización anual del piso (%)", -3.0, 8.0, step=0.5, key="revalorizacion")

    st.header("🔑 Alquiler")
    st.number_input("Alquiler mensual (€)", min_value=100.0, step=50.0, format="%.0f", key="alquiler")
    st.slider("Subida anual del alquiler (%)", 0.0, 8.0, step=0.5, key="subida")
    st.slider("Rentabilidad si inviertes la entrada (%)", 0.0, 10.0, step=0.5,
              key="rentabilidad")

    st.button("↺ Volver a los datos de Madrid", on_click=restablecer_madrid,
              width="stretch")

s = st.session_state

# Validación (como las excepciones de entrada.py: avisamos en vez de rompernos)
if s["entrada"] >= s["precio"]:
    st.error("La entrada tiene que ser menor que el precio del piso.")
    st.stop()

compra, alquiler = crear_objetos(s["precio"], s["entrada"], s["interes"], s["años"],
                                 s["gastos_compra"], s["gastos_anuales"], s["revalorizacion"],
                                 s["alquiler"], s["subida"], s["rentabilidad"])
cruce = año_de_cruce(compra, alquiler)

# ---------------------------------------------------------------------
# Cabecera y respuesta
# ---------------------------------------------------------------------
st.title("¿Comprar o alquilar una vivienda en Madrid?")
st.caption("Proyecto de Programación I · Grado en Análisis de Datos y Negocios (UFV) · "
           "Miguel Poudereux")

if cruce is None:
    titulo = "Con estos datos, en 40 años nunca compensa comprar"
    detalle = "Alquilar e invertir la entrada sale más barato durante todo el periodo."
elif cruce == 1:
    titulo = "Comprar compensa desde el primer año"
    detalle = "Desde el principio, comprar te cuesta menos que alquilar."
else:
    titulo = f"Comprar compensa a partir del año {cruce}"
    detalle = (f"Si piensas quedarte menos de {cruce} años, te sale mejor alquilar. "
               f"Si te quedas más, mejor comprar.")

st.markdown(f'<div class="respuesta"><h2>{titulo}</h2><p>{detalle}</p></div>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
diferencia = compra.cuota() - alquiler.alquiler_mensual
c1.metric("Cuota de la hipoteca", euros(compra.cuota()) + "/mes",
          f"{euros(diferencia)} vs alquiler", delta_color="inverse")
c2.metric("Alquiler", euros(alquiler.alquiler_mensual) + "/mes")
c3.metric("Coste real de comprar (10 años)", euros(compra.coste_total(10)))
c4.metric("Coste real de alquilar (10 años)", euros(alquiler.coste_total(10)))

# ---------------------------------------------------------------------
# Pestañas
# ---------------------------------------------------------------------
t1, t2, t3, t4, t5 = st.tabs(["📈 Comprar vs alquilar", "🏠 Patrimonio",
                              "🧪 ¿Y si...?", "📋 Año a año", "💾 Escenarios"])

# --- 1. Gráfica de costes (la misma idea que grafica_costes) ---------
with t1:
    horizonte = st.slider("Años a mostrar", 5, 40, 30, key="horizonte")
    años_lista = list(range(1, horizonte + 1))
    costes_compra = [compra.coste_total(a) for a in años_lista]
    costes_alquiler = [alquiler.coste_total(a) for a in años_lista]

    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.plot(años_lista, costes_compra, color=AZUL, linewidth=2.5, label="Comprar")
    ax.plot(años_lista, costes_alquiler, color=NARANJA, linewidth=2.5, label="Alquilar")
    if cruce is not None and cruce <= horizonte:
        ax.axvline(cruce, color="gray", linestyle="--")
        ax.annotate(f" Compensa comprar\n desde el año {cruce}", xy=(cruce, 0),
                    xycoords=("data", "axes fraction"), xytext=(cruce, 0.82),
                    textcoords=("data", "axes fraction"), color="#333333")
    ax.axhline(0, color="#BBBBBB", linewidth=0.8)
    ax.set_xlabel("Años")
    ax.set_ylabel("Coste acumulado (€)")
    ax.yaxis.set_major_formatter(lambda v, _: euros(v))
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    st.pyplot(fig)
    st.caption("Coste real = lo que has pagado − lo que te queda (el piso, o el dinero "
               "invertido si alquilas). Un coste negativo significa que has ganado dinero.")

# --- 2. Gráfica de patrimonio (la misma idea que grafica_patrimonio) -
with t2:
    años_lista = list(range(0, compra.años + 1))
    valores = [compra.valor_piso(a) for a in años_lista]
    deudas = [compra.deuda(a) for a in años_lista]

    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.plot(años_lista, valores, color=AZUL, linewidth=2.5, label="Valor del piso")
    ax.plot(años_lista, deudas, color=NARANJA, linewidth=2.5, label="Deuda con el banco")
    ax.fill_between(años_lista, deudas, valores, color=VERDE, alpha=0.15,
                    label="Lo que es tuyo")
    ax.set_xlabel("Años")
    ax.set_ylabel("Euros (€)")
    ax.yaxis.set_major_formatter(lambda v, _: euros(v))
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    st.pyplot(fig)

    a = min(10, compra.años)
    st.info(f"A los {a} años el piso vale **{euros(compra.valor_piso(a))}** y debes "
            f"**{euros(compra.deuda(a))}**: ya es tuyo **{euros(compra.valor_piso(a) - compra.deuda(a))}**.")

# --- 3. Análisis de sensibilidad -------------------------------------
with t3:
    st.subheader("¿Y si el piso sube más o menos, o la inversión rinde distinto?")
    st.write("Cada casilla es el año a partir del cual compensa comprar, con el resto de "
             "datos iguales. Se calcula llamando a `año_de_cruce` para cada combinación.")

    revalorizaciones = [-1.0, 0.0, 1.0, 2.0, 2.5, 3.0, 4.0]
    rentabilidades = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    filas = {}
    for r in revalorizaciones:
        fila = {}
        for inv in rentabilidades:
            c, alq = crear_objetos(s["precio"], s["entrada"], s["interes"], s["años"],
                                   s["gastos_compra"], s["gastos_anuales"], r,
                                   s["alquiler"], s["subida"], inv)
            fila[f"Inversión {inv:g} %"] = año_de_cruce(c, alq)
        filas[f"Piso sube {r:g} %"] = fila
    años_tabla = pd.DataFrame(filas).T          # números (o None si nunca compensa)

    def color(valor):
        """Verde si compensa pronto, amarillo si tarda, rojo si tarda mucho o nunca."""
        if valor is None or pd.isna(valor):
            return "background-color: #F4CCCC; color: #8B0000"
        if valor <= 5:
            return "background-color: #B7E1CD"
        if valor <= 12:
            return "background-color: #FFF2CC"
        return "background-color: #FCE5CD"

    textos = años_tabla.map(lambda v: "nunca" if v is None or pd.isna(v) else f"año {int(v)}")
    estilo = textos.style.apply(lambda _: años_tabla.map(color), axis=None)
    st.dataframe(estilo, width="stretch")
    st.caption("Verde: compensa comprar en 5 años o menos · Amarillo: entre 6 y 12 · "
               "Naranja: más de 12 · Rojo: nunca en 40 años.")

# --- 4. Tabla año a año ----------------------------------------------
with t4:
    datos = []
    for año in range(1, 41):
        cc = compra.coste_total(año)
        ca = alquiler.coste_total(año)
        datos.append({"Año": año,
                      "Coste comprar": euros(cc),
                      "Coste alquilar": euros(ca),
                      "Ahorro si compras": euros(ca - cc),
                      "Mejor opción": "Comprar" if cc < ca else "Alquilar"})
    st.dataframe(pd.DataFrame(datos), hide_index=True, width="stretch", height=520)

# --- 5. Guardar y cargar (usa ficheros.py) ---------------------------
with t5:
    izq, der = st.columns(2)
    with izq:
        st.subheader("Guardar el escenario actual")
        nombre = st.text_input("Nombre del escenario", placeholder="por ejemplo: madrid")
        if st.button("💾 Guardar"):
            if nombre.strip() == "":
                st.warning("Escribe un nombre para el escenario.")
            elif ";" in nombre:
                st.warning("El nombre no puede tener ';' (es el separador del CSV).")
            else:
                guardar_escenario(nombre.strip(), compra, alquiler)
                st.success(f"Escenario '{nombre.strip()}' guardado en escenarios.csv")
    with der:
        st.subheader("Cargar un escenario guardado")
        escenarios = cargar_escenarios()
        if not escenarios:
            st.info("Todavía no hay escenarios guardados.")
        else:
            elegido = st.selectbox("Escenarios en escenarios.csv", list(escenarios.keys()))
            c, alq = escenarios[elegido]
            r = año_de_cruce(c, alq)
            st.write(f"Precio {euros(c.precio)} · alquiler {euros(alq.alquiler_mensual)}/mes · "
                     f"compensa comprar: **{'nunca' if r is None else f'desde el año {r}'}**")
            st.button("📂 Cargar en la web", on_click=aplicar_escenario, args=(c, alq))