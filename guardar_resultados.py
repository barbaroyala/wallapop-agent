from bs4 import BeautifulSoup
import pandas as pd

def extraer_datos(driver, producto_objetivo):
    print("📥 Extrayendo HTML con BeautifulSoup...")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    tarjetas = soup.select('a[href^="/item/"]')

    if not tarjetas:
        print("⚠️ BeautifulSoup no encontró productos.")
        with open(f"html_debug_{producto_objetivo.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
            f.write(html)
        return pd.DataFrame()

    datos = []
    for a in tarjetas:
        try:
            img_tag = a.find("img")
            titulo = img_tag.get("alt", "").strip() if img_tag else "Sin título"
            imagen = img_tag.get("src") if img_tag else ""

            enlace = a.get("href")
            if enlace and not enlace.startswith("http"):
                enlace = "https://es.wallapop.com" + enlace

            precio_tag = a.find("strong", {"aria-label": "Item price"})
            precio = precio_tag.text.strip().replace('\xa0€', ' €') if precio_tag else "N/A"

            datos.append({
                "Producto objetivo": producto_objetivo,
                "Título": titulo,
                "Precio": precio,
                "Enlace": enlace,
                "Imagen": imagen
            })
        except Exception as e:
            print("⚠️ Error en producto:", e)
            continue

    df = pd.DataFrame(datos)
    print(f"✅ Productos extraídos: {len(df)}")
    return df
