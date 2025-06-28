# Busqueda_de_Productos.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Chrome_Driver import crear_driver  # 👈 usa el headless aquí
import time

def buscar_productos(producto: str):
    driver = crear_driver()  # 👈 ahora se usará headless automáticamente
    driver.get("https://es.wallapop.com/")

    # Aceptar cookies
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar todo")]'))
        ).click()
        print("✅ Consentimiento de cookies aceptado.")
    except:
        print("ℹ️ No se mostraron cookies.")

    # Buscar input y enviar término
    try:
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchbox-form-input"))
        )
        input_box.clear()
        input_box.send_keys(producto)
        input_box.submit()
        print("✅ Búsqueda enviada")
    except Exception as e:
        print("❌ Error al buscar:", e)
        driver.quit()
        return None

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="/item/"]'))
        )
    except:
        print("❌ Timeout esperando visibilidad de productos.")

    time.sleep(1)
    return driver
