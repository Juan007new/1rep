from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Modo sin GUI
chrome_options.add_argument('--disable-gpu')  # Deshabilitar GPU (para evitar problemas en servidores)
chrome_options.add_argument('--no-sandbox')  # Solucionar problemas en contenedores
chrome_options.add_argument('--remote-debugging-port=9222')  # Puerto para depuración

# Especificar la ubicación binaria de Chromium (asegúrate de que esté instalada en esa ruta)
chrome_options.binary_location = '/usr/bin/chromium'  # Ajusta esta ruta según el entorno

# Configuración del servicio de Selenium para ChromeDriver
service = Service(ChromeDriverManager().install())

try:
    # Iniciar el navegador Chrome
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Verificar la conexión visitando una página web
    driver.get('https://www.google.com')  # O cualquier página de prueba

    # Imprimir el título de la página para confirmar que todo está funcionando
    print(f"Página cargada correctamente: {driver.title}")
    
except Exception as e:
    print(f"Ocurrió un error: {str(e)}")
finally:
    if driver:
        driver.quit()  # Asegurarse de cerrar el navegador después de ejecutar
