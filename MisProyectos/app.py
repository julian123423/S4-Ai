import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="App Contable Didáctica", layout="wide")

# Inicialización
if "diario" not in st.session_state:
    st.session_state.diario = []

st.title("📚 Aplicación Contable Didáctica")
st.markdown("### Sistema de registro contable con Arqueo de Caja, Estado de Resultados y más")

# === Sección 1: Arqueo de Caja (detallado como en la imagen) ===
st.header("💵 Arqueo de Caja al estilo tradicional")

billetes = [500, 200, 100, 50, 20]
monedas = [10, 5, 2, 1]

with st.form("arqueo_detallado"):
    st.subheader("🧾 Billetes")
    total_billetes = 0
    billete_cantidades = {}
    for b in billetes:
        cantidad = st.number_input(f"${b} x", min_value=0, step=1, key=f"b_{b}")
        total = b * cantidad
        total_billetes += total
        billete_cantidades[f"${b}"] = {"Cantidad": cantidad, "Total": total}

    st.subheader("🪙 Monedas")
    total_monedas = 0
    moneda_cantidades = {}
    for m in monedas:
        cantidad = st.number_input(f"${m} x", min_value=0, step=1, key=f"m_{m}")
        total = m * cantidad
        total_monedas += total
        moneda_cantidades[f"${m}"] = {"Cantidad": cantidad, "Total": total}

    submit_arqueo = st.form_submit_button("Calcular Total")

if submit_arqueo:
    total_arqueo = total_billetes + total_monedas
    st.success("✅ Arqueo calculado correctamente")
    st.subheader("📋 Detalle del arqueo")

    st.markdown("**Billetes**")
    df_billetes = pd.DataFrame(billete_cantidades).T
    st.dataframe(df_billetes)

    st.markdown("**Monedas**")
    df_monedas = pd.DataFrame(moneda_cantidades).T
    st.dataframe(df_monedas)

    st.metric("💰 Total en Caja", f"${total_arqueo:,.2f}")

# === Sección 2: Registro Diario ===
st.header("📘 Registro Diario")
with st.form("registro_diario"):
    c1, c2, c3 = st.columns(3)
    with c1:
        fecha = st.date_input("Fecha", value=date.today())
    with c2:
        cuenta = st.text_input("Cuenta contable")
    with c3:
        descripcion = st.text_input("Descripción")

    c4, c5 = st.columns(2)
    with c4:
        debe = st.number_input("Debe", min_value=0.0, step=0.01)
    with c5:
        haber = st.number_input("Haber", min_value=0.0, step=0.01)

    submit_diario = st.form_submit_button("Agregar asiento")

if submit_diario:
    if not cuenta.strip():
        st.error("❌ La cuenta contable no puede estar vacía")
    elif debe == 0 and haber == 0:
        st.warning("⚠️ Debe registrar un valor en 'Debe' o 'Haber'")
    else:
        st.session_state.diario.append({
            "Fecha": fecha, "Cuenta": cuenta.title(), "Descripción": descripcion,
            "Debe": debe, "Haber": haber
        })
        st.success("✅ Asiento agregado correctamente")

df_diario = pd.DataFrame(st.session_state.diario)
if not df_diario.empty:
    st.subheader("📋 Asientos registrados")
    st.dataframe(df_diario, use_container_width=True)

# === Sección 3: Libro Mayor ===
st.header("📒 Libro Mayor")
if not df_diario.empty:
    mayor = df_diario.groupby("Cuenta")[["Debe", "Haber"]].sum()
    mayor["Saldo"] = mayor["Debe"] - mayor["Haber"]
    st.dataframe(mayor, use_container_width=True)

# === Sección 4: Balanza de Comprobación ===
st.header("📗 Balanza de Comprobación")
if not df_diario.empty:
    balanza = mayor.copy()
    balanza["Debe"] = balanza["Debe"].apply(lambda x: x if x > 0 else 0)
    balanza["Haber"] = balanza["Haber"].apply(lambda x: x if x > 0 else 0)
    st.dataframe(balanza, use_container_width=True)

# === Sección 5: Estado de Resultados (Procedimiento Analítico) ===
st.header("📈 Estado de Resultados (Procedimiento Analítico)")
if not df_diario.empty:
    ingresos = df_diario[df_diario["Cuenta"].str.contains("venta", case=False)]["Haber"].sum()
    costos = df_diario[df_diario["Cuenta"].str.contains("costo", case=False)]["Debe"].sum()
    gastos = df_diario[df_diario["Cuenta"].str.contains("gasto", case=False)]["Debe"].sum()
    utilidad = ingresos - costos - gastos

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ingresos", f"${ingresos:.2f}")
    col2.metric("Costos", f"${costos:.2f}")
    col3.metric("Gastos", f"${gastos:.2f}")
    col4.metric("Utilidad Neta", f"${utilidad:.2f}", delta_color="inverse" if utilidad < 0 else "normal")

# === Reporte técnico ===
st.markdown("---")
st.subheader("📝 Reporte de funcionamiento")
st.markdown("""
- El arqueo de caja sigue el formato tradicional con cantidades y totales por denominación.
- Permite registrar asientos contables en un diario digital.
- Se generan automáticamente el Libro Mayor, Balanza de Comprobación y Estado de Resultados.
- Visualización clara con métricas, tablas y validaciones interactivas.
""")
