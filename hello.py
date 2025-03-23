from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pyperclip  # You'll need to install this: pip install pyperclip

print("Script started - Setting up Chrome driver options...")

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-webrtc")

print("Setting up Chrome driver path...")
chromedriver_path = os.path.abspath(r"S:\creuto\chromedriver-win64\chromedriver-win64\chromedriver.exe")
service = Service(executable_path=chromedriver_path)

# Initialize the Chrome driver
try:
    print("Initializing Chrome driver...")
    driver = webdriver.Chrome(service=service, options=options)
    print(f"Successfully initialized Chrome driver with path: {chromedriver_path}")
    time.sleep(2)  # Added delay
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    exit(1)

# Go directly to the LinkedIn login page
try:
    print("Navigating to LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")
    print("Successfully navigated to LinkedIn login page")
    time.sleep(5)  # Increased delay to 5 seconds
except Exception as e:
    print(f"Error navigating to LinkedIn login: {e}")
    driver.quit()
    exit(1)

# Get login credentials securely
try:
    username = "camiadonelby@hotmail.com"
    password = "cami@1234"
    
    print("Waiting for username field to become available...")
    # Wait for username field and enter credentials
    email_field = WebDriverWait(driver, 15).until(  # Increased timeout
        EC.presence_of_element_located((By.ID, "username"))
    )
    print("Entering username...")
    email_field.send_keys(username)
    time.sleep(2)  # Added delay
    
    print("Entering password...")
    # Find password field and enter credentials
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    time.sleep(2)  # Added delay
    
    print("Clicking sign-in button...")
    # Click the sign-in button
    sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    sign_in_button.click()
    
    print("Login credentials entered and form submitted")
    
    # Wait for login to complete
    print("Waiting for login to complete...")
    WebDriverWait(driver, 20).until(  # Increased timeout
        EC.url_contains("linkedin.com/feed")
    )
    print("Successfully logged in!")
    time.sleep(5)  # Added delay after login
    
except Exception as e:
    print(f"Error during login process: {e}")
    driver.quit()
    exit(1)

# Navigate to feed page if not already there
if "linkedin.com/feed" not in driver.current_url:
    try:
        print("Navigating to LinkedIn feed page...")
        driver.get("https://www.linkedin.com/feed/")
        print("Navigated to LinkedIn feed page")
        time.sleep(5)  # Added delay
    except Exception as e:
        print(f"Error navigating to feed: {e}")
        driver.quit()
        exit(1)

# Navigate to the Flutter search results
try:
    print("Navigating to Flutter search results page...")
    search_url = "https://www.linkedin.com/search/results/content/?keywords=flutter&origin=FACETED_SEARCH&sid=TT5&sortBy=%22date_posted%22"
    driver.get(search_url)
    print("Successfully navigated to Flutter search results")
    time.sleep(8)  # Added longer delay to ensure page loads fully
except Exception as e:
    print(f"Error navigating to search results: {e}")
    driver.quit()
    exit(1)

# Function to extract links for posts
def extract_post_links(num_posts=5):
    post_links = []
    
    # Find all posts
    print(f"Searching for posts on the page...")
    try:
        posts = WebDriverWait(driver, 15).until(  # Increased timeout
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'feed-shared-update-v2') or contains(@class, 'search-content-card')]"))
        )
        
        print(f"Found {len(posts)} posts, extracting links for first {min(num_posts, len(posts))} posts")
    except Exception as e:
        print(f"Error finding posts: {e}")
        return post_links
    
    # Process only the first num_posts
    for i, post in enumerate(posts[:num_posts]):
        try:
            print(f"\n--- Processing post {i+1}/{min(num_posts, len(posts))} ---")
            
            # Scroll post into view
            print(f"Scrolling post {i+1} into view...")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post)
            time.sleep(3)  # Increased delay for scrolling
            
            # Find three-dots menu button and click
            print(f"Looking for three-dots menu on post {i+1}...")
            
            # Try different approaches to find the three dots button
            try:
                three_dots_button = post.find_element(By.XPATH, ".//button[contains(@class, 'artdeco-dropdown__trigger') or contains(@class, 'feed-shared-control-menu__trigger')]")
                print(f"Found three-dots menu button using primary selector")
            except:
                try:
                    # Try alternate approach - look for the SVG
                    three_dots_button = post.find_element(By.XPATH, ".//button[.//li-icon[@type='overflow-web-ios']]")
                    print(f"Found three-dots menu button using SVG selector")
                except:
                    # Try another alternate approach - any button with no text that might be a menu
                    buttons = post.find_elements(By.XPATH, ".//button")
                    three_dots_button = None
                    for button in buttons:
                        if not button.text and button.is_displayed():
                            three_dots_button = button
                            break
                    
                    if three_dots_button is None:
                        print(f"Could not find three-dots menu button for post {i+1}")
                        continue
                    print(f"Found three-dots menu button using fallback method")
            
            print(f"Clicking three-dots menu...")
            three_dots_button.click()
            time.sleep(3)  # Increased delay after clicking
            
            # Find "Copy link to post" option - there are multiple approaches to find this
            print(f"Looking for 'Copy link to post' option...")
            try:
                # Try first approach - by text content
                copy_link_option = WebDriverWait(driver, 8).until(  # Increased timeout
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'artdeco-dropdown__content')]//li[contains(., 'Copy link to post') or contains(., 'Copy link')]"))
                )
                print(f"Found 'Copy link to post' option by text content")
            except:
                try:
                    # Try another approach - by aria-label
                    copy_link_option = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'artdeco-dropdown__content')]//li[@aria-label='Copy link to post']"))
                    )
                    print(f"Found 'Copy link to post' option by aria-label")
                except:
                    # Alternative approach - by expected position in menu
                    print(f"Trying to find 'Copy link' by menu position...")
                    time.sleep(2)
                    menu_options = driver.find_elements(By.XPATH, "//div[contains(@class, 'artdeco-dropdown__content')]//li")
                    print(f"Found {len(menu_options)} menu options")
                    
                    if len(menu_options) >= 2:  # Assuming "Copy link" is usually the 2nd option
                        copy_link_option = menu_options[1]
                        print(f"Selected menu item at position 2")
                    else:
                        print(f"Not enough menu options found for post {i+1}")
                        continue
            
            # Click the copy link option
            print(f"Clicking 'Copy link to post' option...")
            copy_link_option.click()
            time.sleep(3)  # Increased delay after clicking
            
            # Since copying puts text in clipboard, get it from there
            try:
                post_url = pyperclip.paste()
                print(f"Retrieved from clipboard: {post_url}")
                
                if "linkedin.com" in post_url:
                    post_links.append(post_url)
                    print(f"Successfully extracted URL for post {i+1}: {post_url}")
                else:
                    print(f"Clipboard content does not contain a LinkedIn URL: '{post_url}'")
                    # Fallback: Try to extract post ID and build URL
                    print(f"Trying fallback method to extract post URL...")
                    post_id = post.get_attribute('data-urn') or post.get_attribute('data-id') or ""
                    if post_id:
                        print(f"Found post ID: {post_id}")
                        # Extract the post ID if it's in a format like "urn:li:activity:7176301425224982528"
                        post_id_parts = post_id.split(":")
                        if len(post_id_parts) >= 3:
                            constructed_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id_parts[-1]}"
                            post_links.append(constructed_url)
                            print(f"Successfully constructed URL for post {i+1}: {constructed_url}")
                        else:
                            print(f"Could not parse post ID format: {post_id}")
                    else:
                        print(f"Could not find post ID for post {i+1}")
            except Exception as e:
                print(f"Error extracting URL for post {i+1}: {e}")
                
            # Close any open dropdown menu by clicking elsewhere
            print(f"Closing dropdown menu...")
            driver.execute_script("document.body.click();")
            time.sleep(3)  # Increased delay after closing dropdown
                
        except Exception as e:
            print(f"Error processing post {i+1}: {e}")
    
    return post_links

# Extract links for the first 10 posts
print("\nStarting extraction of post links...")
post_links = extract_post_links(10)

# Print a summary of all links
print("\n--- SUMMARY - All extracted post links ---")
if post_links:
    for i, link in enumerate(post_links):
        print(f"{i+1}. {link}")
    print(f"\nSuccessfully extracted {len(post_links)} post links")
else:
    print("No post links were successfully extracted")

# Don't close the browser immediately
input("\nScript complete. Press Enter to close the browser...")
driver.quit()