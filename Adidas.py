from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

def get_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = '/usr/bin/chromium-browser'
    return chrome_options

def main():
    print("Starting Selenium script...")
    try:
        service = Service('/usr/bin/chromedriver')
        options = get_chrome_options()
        
        print("Initializing Chrome driver...")
        driver = webdriver.Chrome(service=service, options=options)
        
        print("Navigating to website...")
        driver.get("https://www.google.com")
        
        # Wait for page to load
        time.sleep(2)
        
        print(f"Successfully loaded page. Title: {driver.title}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e
    
    finally:
        if 'driver' in locals():
            driver.quit()
            print("Chrome driver closed successfully")

if __name__ == "__main__":
    main()
