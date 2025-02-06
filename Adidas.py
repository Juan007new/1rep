from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
chrome_options.add_argument("--disable-gpu")  # Desactivar GPU para modo headless
chrome_options.add_argument("--no-sandbox")  # Evitar el modelo de seguridad del OS
chrome_options.add_argument("--disable-dev-shm-usage")  # Solucionar problemas de recursos limitados

# Especificar la ruta a ChromeDriver
chrome_driver_path = "./chromedriver"  # Asegúrate de que el archivo esté en la raíz del proyecto

# Inicializar el navegador usando Service
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Abrir Google
driver.get("https://www.google.com")

# Imprimir el título de la página
print("Título de la página:", driver.title)

# Cerrar el navegador
driver.quit()
