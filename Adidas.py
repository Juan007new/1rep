from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import json
import random
import urllib.parse

def telegram_bot_sendtext(bot_message, image_url=None):
    """Envía un mensaje y una imagen opcional al bot de Telegram."""
    #bot_token = '7693801036:AAF8V_3EA74x-hfXk2DpRoY6hm2-_x9fx44'
    #bot_chatID = '1507772195'
    
    # Primero enviar la imagen si existe
    enviar_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(enviar_text)
    return response.json()

def check_availability(driver, product_url):
    """Verifica la disponibilidad del producto visitando su página."""
    try:
        driver.get(product_url)
        time.sleep(random.uniform(2, 3))  # Espera aleatoria para evitar detección
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Verificar si aparece el mensaje "Próximamente disponible"
        coming_soon = soup.find('h2', {'class': 'sold-out-callout_title___1u2ms'})
        if coming_soon and 'Próximamente disponible' in coming_soon.text:
            return "Próximamente disponible"
        
        return "Disponible"
            
    except Exception as e:
        print(f"Error al verificar disponibilidad: {str(e)}")
        return "Estado no disponible"

def extract_price(price_element):
    """Extrae el precio desde un elemento HTML."""
    if price_element:
        price_text = price_element.text.strip().replace("S/", "").replace(" ", "").replace(",", "")
        try:
            return float(price_text)
        except ValueError:
            return 0
    return 0

def setup_driver():
    """Configura y retorna el driver de Selenium con medidas anti-detección."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """
        }
    )
    return driver

def extract_product_info(product, driver):
    """Extrae la información básica del producto desde el HTML."""
    name_element = product.find('p', class_='product-card-description_name__xHvJ2')
    product_name = name_element.text.strip() if name_element else 'Nombre no disponible'
    
    category_elements = product.find_all('p', class_='product-card-description_info__z_CcT')
    category = category_elements[0].text.strip() if category_elements else ''
    
    sale_price = extract_price(product.find('div', class_='gl-price-item--sale'))
    original_price = extract_price(product.find('del')) or sale_price
    
    link_element = product.find('a', href=True)
    product_link = f"https://www.adidas.pe{link_element['href']}" if link_element else 'Enlace no disponible'
    
    # Verificar disponibilidad
    availability = check_availability(driver, product_link) if product_link != 'Enlace no disponible' else 'Estado no disponible'
    
    return {
        'name': product_name,
        'category': category,
        'original_price': original_price,
        'sale_price': sale_price,
        'discount_percentage': round((1 - sale_price / original_price) * 100, 2) if original_price > 0 else 0,
        'product_link': product_link,
        'availability': availability
    }

def main():
    try:
        driver = setup_driver()
        #url_base = 'https://www.adidas.pe/zapatillas-mujer?sale_percentage_es_pe=65'
        print("Accediendo a la página...")
        driver.get(url_base)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'glass-gdpr-default-consent-accept-button'))
            ).click()
            print("Cookies aceptadas correctamente.")
        except Exception as e:
            print("No se encontró el popup de cookies o ya se aceptaron.")

        print("Cargando todos los productos...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("Extrayendo información de productos...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all('article', class_='product-card_product-card__a9BIh')
        all_products = []

        for product in products:
            product_data = extract_product_info(product, driver)
            all_products.append(product_data)
            if product_data['availability']==f"Disponible":
              if product_data['discount_percentage'] >= 65:
                message = ( 
                    f"🏷️ *{product_data['name']}*\n\n"
                    f"📍 Categoría: {product_data['category']}\n"
                    f"💰 Descuento: {product_data['discount_percentage']}%\n"
                    f"💎 Precio final: S/{product_data['sale_price']:.2f}\n"
                    f"📌 Precio original: S/{product_data['original_price']:.2f}\n"
                    f"✨ Estado: {product_data['availability']}\n"
                    f" link:{product_data['product_link']}"
                )
                telegram_bot_sendtext(message)

        with open('adidas_products.json', 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)
            print("\nResultados guardados en 'adidas_products.json'")

    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
    finally:
        print("\nCerrando el navegador...")
        driver.quit()

if __name__ == "__main__":
    main()
