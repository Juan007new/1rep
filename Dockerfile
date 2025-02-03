from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
chrome_options.add_argument("--no-sandbox")  # Avoid OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Fix limited resource issues

# Initialize the browser
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open Google
    driver.get("https://www.google.com")
    # Print page title
    print("Page title:", driver.title)

finally:
    # Close the browser
    driver.quit()
