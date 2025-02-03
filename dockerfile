# Usar la imagen oficial de Selenium con Chrome
FROM selenium/standalone-chrome:latest

# Instalar Python y pip
RUN sudo apt-get update && sudo apt-get install -y python3 python3-pip

# Copiar el código de tu aplicación al contenedor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
chrome_options.add_argument("--disable-gpu")  # Desactivar GPU para modo headless
chrome_options.add_argument("--no-sandbox")  # Evitar el modelo de seguridad del OS
chrome_options.add_argument("--disable-dev-shm-usage")  # Solucionar problemas de recursos limitados

# Inicializar el navegador
driver = webdriver.Chrome(options=chrome_options)

# Abrir Google
driver.get("https://www.google.com")

# Imprimir el título de la página
print("Título de la página:", driver.title)

# Cerrar el navegador
driver.quit()

# Instalar las dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Comando para ejecutar tu aplicación
CMD ["python3", "Adidas.py"]
