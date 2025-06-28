from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import shutil

def crear_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Detectar Chromium en el sistema
    chrome_path = shutil.which("chromium") or shutil.which("chromium-browser")
    chrome_options.binary_location = chrome_path

    # Selenium Manager se encarga del ChromeDriver
    return webdriver.Chrome(options=chrome_options)
