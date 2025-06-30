import streamlit as st
import pandas as pd
from main import ejecutar_agente
from analisis_ofertas import analizar_ofertas
import os

st.set_page_config(page_title="Agente de Reventa Wallapop", layout="wide")

st.title("🛍️ Agente de Reventa para Wallapop")
st.markdown("Este agente busca productos, los analiza según tu estrategia y te muestra las mejores oportunidades de reventa.")

# === Mostrar siempre el último resultado si existe ===
if os.path.exists("ofertas_filtradas.csv"):
    df = pd.read_csv("ofertas_filtradas.csv")
    st.subheader("🔍 Últimos resultados disponibles")
    top5 = df.sort_values(by="Diferencia (%)", ascending=False).head(5)

    columnas = [
        "Producto objetivo", "Título", "Precio limpio",
        "Precio objetivo", "Diferencia (%)", "Riesgo detectado", "Enlace"
    ]

    st.subheader("🔝 Top 5 Mejores Ofertas")
    st.dataframe(top5[columnas])

    csv_top5 = top5[columnas].to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button("⬇️ Descargar Top 5", data=csv_top5, file_name="top5_ofertas.csv", mime="text/csv")

    st.subheader("📦 Todas las Ofertas Filtradas")
    st.dataframe(df)

    csv_full = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button("⬇️ Descargar todas las ofertas", data=csv_full, file_name="ofertas_filtradas.csv", mime="text/csv")
else:
    st.info("🔍 Aún no se ha generado ningún resultado.")

# === Ejecutar búsqueda si el usuario lo pide ===
if st.button("🔁 Ejecutar nueva búsqueda y análisis"):
    with st.spinner("Ejecutando scraping, extracción y análisis..."):
        ejecutar_agente()
    st.success("✅ Proceso completado. Recarga para ver los nuevos resultados.")
