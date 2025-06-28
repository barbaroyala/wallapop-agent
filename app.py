import streamlit as st
import pandas as pd
from main import ejecutar_agente
from analisis_ofertas import analizar_ofertas

st.set_page_config(page_title="Agente de Reventa Wallapop", layout="wide")

st.title("🛍️ Agente de Reventa para Wallapop")
st.markdown("Este agente busca productos, los analiza según tu estrategia y te muestra las mejores oportunidades de reventa.")

# Botón para lanzar el scraping y análisis
if st.button("🔍 Ejecutar agente de búsqueda y análisis"):
    with st.spinner("Ejecutando scraping, extracción y análisis..."):
        ejecutar_agente()

    st.success("✅ Proceso completado.")
    
    # Cargar resultados
    try:
        df = pd.read_csv("ofertas_filtradas.csv")
        top5 = df.sort_values(by="Diferencia (%)", ascending=False).head(5)

        st.subheader("🔝 Top 5 Mejores Ofertas")
        st.dataframe(top5[[
            "Producto objetivo", "Título", "Precio limpio",
            "Precio objetivo", "Diferencia (%)", "Riesgo detectado", "Enlace"
        ]])

        # Botón de descarga Top 5
        csv_top5 = top5.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("⬇️ Descargar Top 5 en CSV", data=csv_top5, file_name="top5_ofertas.csv", mime="text/csv")

        st.subheader("📦 Todas las ofertas filtradas")
        st.dataframe(df)

        # Botón de descarga completa
        csv_full = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("⬇️ Descargar todas las ofertas", data=csv_full, file_name="ofertas_filtradas.csv", mime="text/csv")

    except FileNotFoundError:
        st.warning("⚠️ No se encontraron resultados. Ejecuta el agente primero.")

else:
    st.info("Haz clic en el botón para comenzar la búsqueda y análisis.")
    
#streamlit run app.py
