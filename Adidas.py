import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def setup_chrome():
    print("Configurando opciones de Chrome...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/chromium-browser'  # Especificamos la ubicación del binario
    return options

def create_driver():
    options = setup_chrome()
    print("Opciones de Chrome configuradas")
    
    # Configurar el servicio de Chrome
    service = Service('/usr/bin/chromedriver')
    print("Servicio de Chrome configurado")
    
    return webdriver.Chrome(service=service, options=options)

def main():
    print("Iniciando script...")
    driver = None
    
    try:
        # Verificar existencia del binario de Chrome
        if not os.path.exists('/usr/bin/chromium-browser'):
            print("Error: No se encuentra el binario de Chrome en /usr/bin/chromium-browser")
            return
        
        # Verificar existencia del chromedriver
        if not os.path.exists('/usr/bin/chromedriver'):
            print("Error: No se encuentra chromedriver en /usr/bin/chromedriver")
            return
        
        # Inicializar el driver
        print("Inicializando Chrome driver...")
        driver = create_driver()
        print("Chrome driver inicializado exitosamente")
        
        # Navegar a la página
        print("Navegando a Google...")
        driver.get("https://www.google.com")
        print(f"Página cargada. Título: {driver.title}")
        
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        raise e
    
    finally:
        if driver:
            print("Cerrando Chrome driver...")
            driver.quit()
            print("Chrome driver cerrado exitosamente")

if __name__ == "__main__":
    main()
