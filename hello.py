from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import os
import pyperclip 

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

# Function to extract links for posts - FIXED VERSION
def extract_post_links(num_posts=5):
    post_links = []
    collected_urls = set()  # Keep track of URLs we've already seen
    
    # Find all posts
    print(f"Searching for posts on the page...")
    try:
        # Wait for the search results to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results__cluster-content')]"))
        )
        
        # Scroll down a bit to load more content
        print("Scrolling to load more content...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(3)
        
        # Use a more specific XPath for search result posts
        post_containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'search-content-card')]")
        print(f"Found {len(post_containers)} post containers")
        
        # If no results with that class, try the alternative
        if not post_containers:
            post_containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")
            print(f"Found {len(post_containers)} posts using alternative selector")
        
        # If we still don't have posts, try a more generic approach
        if not post_containers:
            post_containers = driver.find_elements(By.XPATH, "//div[contains(@data-id, 'urn:li:activity:')]")
            print(f"Found {len(post_containers)} posts using data-id selector")
            
        print(f"Will process up to {min(num_posts, len(post_containers))} posts")
    except Exception as e:
        print(f"Error finding posts: {e}")
        return post_links
    
    actions = ActionChains(driver)
    processed_count = 0
    index = 0
    
    # Process posts until we get the number we want or run out
    while processed_count < num_posts and index < len(post_containers):
        try:
            post = post_containers[index]
            index += 1
            print(f"\n--- Processing post {processed_count + 1}/{min(num_posts, len(post_containers))} ---")
            
            # Scroll the post into center view
            print(f"Scrolling post into center view...")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post)
            time.sleep(3)
            
            # Additional small scroll to adjust view
            driver.execute_script("window.scrollBy(0, -50);")
            time.sleep(1)
            
            # Try to find the three-dots menu
            print("Looking for three-dots menu button...")
            three_dots_button = None
            
            # Multiple approaches to find the three-dots button
            try:
                # Look for buttons with overflow icon or dropdown trigger classes
                buttons = post.find_elements(By.XPATH, ".//button[contains(@class, 'artdeco-dropdown__trigger') or .//li-icon[contains(@type, 'overflow')] or .//span[@class='visually-hidden' and contains(text(), 'More actions')]]")
                
                if buttons:
                    # Filter for visible buttons
                    for button in buttons:
                        if button.is_displayed():
                            three_dots_button = button
                            print("Found three-dots button that is displayed")
                            break
                            
                # If still not found, try a more aggressive approach
                if not three_dots_button:
                    # Find all buttons in this post
                    all_buttons = post.find_elements(By.TAG_NAME, "button")
                    print(f"Found {len(all_buttons)} buttons in post")
                    
                    # Look for the last visible button, often the three-dots menu
                    for button in reversed(all_buttons):
                        if button.is_displayed():
                            three_dots_button = button
                            print("Using last visible button as three-dots menu")
                            break
            except Exception as e:
                print(f"Error finding buttons: {e}")
            
            if not three_dots_button:
                print("Could not find three-dots menu button - skipping post")
                continue
                
            # Click the three-dots menu with ActionChains for better precision
            print("Clicking three-dots menu...")
            try:
                actions.move_to_element(three_dots_button).pause(1).click().perform()
                time.sleep(3)
            except Exception as e:
                print(f"Error clicking menu button: {e}")
                # Try JavaScript click as fallback
                try:
                    driver.execute_script("arguments[0].click();", three_dots_button)
                    print("Used JavaScript click as fallback")
                    time.sleep(3)
                except:
                    print("JavaScript click failed too, skipping post")
                    continue
            
            # Find the "Copy link" option
            print("Looking for 'Copy link' option...")
            try:
                # Wait for dropdown menu to appear
                dropdown = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'artdeco-dropdown__content') or contains(@class, 'feed-shared-control-menu__content')]"))
                )
                
                # Look for the copy link option using different approaches
                copy_link_option = None
                
                # Try by text content first
                link_options = dropdown.find_elements(By.XPATH, ".//li[contains(., 'Copy link') or contains(@aria-label, 'Copy link')]")
                if link_options:
                    copy_link_option = link_options[0]
                    print("Found copy link option by text")
                
                # If not found, try by position (usually second option)
                if not copy_link_option:
                    all_options = dropdown.find_elements(By.XPATH, ".//li")
                    if len(all_options) >= 2:
                        copy_link_option = all_options[1]  # Second item is often Copy Link
                        print("Using second menu option as copy link")
                
                if not copy_link_option:
                    print("Could not find copy link option, skipping post")
                    # Close dropdown by clicking elsewhere
                    driver.execute_script("document.body.click();")
                    time.sleep(1)
                    continue
                
                # Click the copy link option with ActionChains
                print("Clicking copy link option...")
                actions.move_to_element(copy_link_option).pause(1).click().perform()
                time.sleep(3)
                
                # Get the URL from clipboard
                clipboard_before = pyperclip.paste()
                print(f"Retrieved from clipboard: {clipboard_before}")
                
                # Verify this is a LinkedIn URL and we haven't seen it before
                if "linkedin.com" in clipboard_before and clipboard_before not in collected_urls:
                    collected_urls.add(clipboard_before)
                    post_links.append(clipboard_before)
                    print(f"Successfully extracted new URL: {clipboard_before}")
                    processed_count += 1
                else:
                    print("URL already collected or not a LinkedIn URL - trying next post")
                
            except Exception as e:
                print(f"Error with copy link option: {e}")
            
            # Always close any dropdown menu by clicking elsewhere
            print("Closing dropdown menu...")
            try:
                driver.execute_script("document.body.click();")
                time.sleep(2)
            except:
                pass
                
        except Exception as e:
            print(f"Error processing post: {e}")
            
        # Scroll a bit to reveal more posts if needed
        if index % 3 == 0:
            print("Scrolling to reveal more posts...")
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(2)
    
    return post_links

# Extract links for posts
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