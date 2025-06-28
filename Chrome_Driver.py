from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import shutil

def crear_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Detectar ruta real de Chromium en Render
    chrome_path = shutil.which("chromium") or shutil.which("chromium-browser")
    chrome_options.binary_location = chrome_path

    # WebDriver manager instalará el ChromeDriver compatible con esa versión
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)
