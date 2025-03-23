from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-webrtc")

chromedriver_path = os.path.abspath(r"S:\creuto\chromedriver-win64\chromedriver-win64\chromedriver.exe")
service = Service(executable_path=chromedriver_path)

# Initialize the Chrome driver
try:
    driver = webdriver.Chrome(service=service, options=options)
    print(f"Successfully initialized Chrome driver with path: {chromedriver_path}")
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    exit(1)

# Go directly to the LinkedIn login page
try:
    driver.get("https://www.linkedin.com/login")
    print("Successfully navigated to LinkedIn login page")
    time.sleep(3)  # Give time to load
except Exception as e:
    print(f"Error navigating to LinkedIn login: {e}")
    driver.quit()
    exit(1)

# Get login credentials securely
try:
    username = "camiadonelby@hotmail.com"
    password = "cami@1234"
    
    # Wait for username field and enter credentials
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.send_keys(username)
    
    # Find password field and enter credentials
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    
    # Click the sign-in button
    sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    sign_in_button.click()
    
    print("Login credentials entered and form submitted")
    
    # Wait for login to complete
    WebDriverWait(driver, 15).until(
        EC.url_contains("linkedin.com/feed")
    )
    print("Successfully logged in!")
    
except Exception as e:
    print(f"Error during login process: {e}")

# # Set headers using Chrome DevTools Protocol (CDP)
# try:
#     driver.execute_cdp_cmd('Network.enable', {})
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
#     }
#     driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': headers})
#     print("Successfully set headers")
# except Exception as e:
#     print(f"Error setting headers: {e}")

# Navigate to feed page if not already there
if "linkedin.com/feed" not in driver.current_url:
    try:
        driver.get("https://www.linkedin.com/feed/")
        print("Navigated to LinkedIn feed page")
    except Exception as e:
        print(f"Error navigating to feed: {e}")

# Don't close the browser immediately
input("Press Enter to close the browser...")
driver.quit()