from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configurar opciones para Chrome en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless
chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU para headless

# Inicializar el navegador
driver = webdriver.Chrome(options=chrome_options)

# Abrir Google
driver.get("https://www.google.com")

# Imprimir el título de la página
print(driver.title)

# Cerrar el navegador
driver.quit()
