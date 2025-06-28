from Busqueda_de_Productos import buscar_productos
from Extraccion_de_Datos import extraer_datos
from Eficiencia_del_Scraping import iniciar_temporizador, terminar_temporizador
from analisis_ofertas import analizar_ofertas
import pandas as pd

# 🧭 Tu estrategia de productos
productos_objetivo = [
    "iPhone 11",
    "Galaxy S8",
    "Nintendo DSi XL",
    "Galaxy Tab S6 Lite",
    "Lenovo Tab M10",
    "PS3 Slim"
]

def ejecutar_agente():
    todos_los_datos = []

    iniciar_temporizador("total")

    for producto in productos_objetivo:
        print(f"\n🔍 Buscando: {producto}")
        iniciar_temporizador(f"búsqueda {producto}")
        driver = buscar_productos(producto)
        terminar_temporizador(f"búsqueda {producto}")

        if driver:
            datos = extraer_datos(driver, producto)
            todos_los_datos.append(datos)
            driver.quit()
        else:
            print(f"❌ No se pudo procesar: {producto}")

    if todos_los_datos:
        df_final = pd.concat(todos_los_datos, ignore_index=True)
        df_final.to_csv("resultados_wallapop.csv", index=False, encoding="utf-8-sig")
        print(f"\n✅ Archivo final guardado: resultados_wallapop.csv")
        print(f"🛍️ Total productos recopilados: {len(df_final)}")

        # 🧠 Ejecutar análisis final
        ejecutar_analisis_final()
    else:
        print("⚠️ No se obtuvieron resultados.")

    terminar_temporizador("total")

def ejecutar_analisis_final():
    tabla_final = analizar_ofertas()
    tabla_final.to_csv("ofertas_filtradas.csv", index=False, encoding="utf-8-sig")
    print("✅ Análisis final guardado en 'ofertas_filtradas.csv'")
    print(f"📉 Total de ofertas detectadas: {len(tabla_final)}")

    # 🔝 Top 5 mejores ofertas
    top5 = tabla_final.sort_values(by="Diferencia (%)", ascending=False).head(5)
    columnas = [
        "Producto objetivo", "Título", "Precio limpio",
        "Precio objetivo", "Diferencia (%)", "Riesgo detectado", "Enlace"
    ]
    print("\n🔝 Top 5 ofertas encontradas:")
    print(top5[columnas].to_string(index=False))

    top5[columnas].to_csv("top5_ofertas.csv", index=False, encoding="utf-8-sig")
    print("✅ Top 5 guardado en 'top5_ofertas.csv'")

if __name__ == "__main__":
    ejecutar_agente()
