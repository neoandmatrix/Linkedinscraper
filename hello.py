from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pyperclip
import urllib.parse

def read_search_terms(file_path):
    """Read search terms from a file, one per line"""
    try:
        with open(file_path, 'r') as file:
            terms = [line.strip() for line in file if line.strip()]
        print(f"Successfully read {len(terms)} search terms from {file_path}")
        return terms
    except Exception as e:
        print(f"Error reading search terms file: {e}")
        return ["flutter"]  # Default search term if file can't be read

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
    time.sleep(5)
except Exception as e:
    print(f"Error navigating to LinkedIn login: {e}")
    driver.quit()
    exit(1)

# Get login credentials securely
try:
    username = "camiadonelby@hotmail.com"
    password = "cami@1234"
    
    print("Waiting for username field to become available...")
    email_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    print("Entering username...")
    email_field.send_keys(username)
    time.sleep(2)
    
    print("Entering password...")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    time.sleep(2)
    
    print("Clicking sign-in button...")
    sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    sign_in_button.click()
    
    print("Login credentials entered and form submitted")
    print("Waiting for login to complete...")
    WebDriverWait(driver, 20).until(
        EC.url_contains("linkedin.com/feed")
    )
    print("Successfully logged in!")
    time.sleep(5)
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
        time.sleep(5)
    except Exception as e:
        print(f"Error navigating to feed: {e}")
        driver.quit()
        exit(1)

# Function to extract links for posts
def extract_post_links(num_posts=5):
    post_links = []
    collected_urls = set()  # Track URLs to avoid duplicates
    
    # Find all posts
    print(f"Searching for posts on the page...")
    try:
        posts = WebDriverWait(driver, 15).until(
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
            time.sleep(3)
            
            # Find three-dots menu button and click
            print(f"Looking for three-dots menu on post {i+1}...")
            
            # Try different approaches to find the three dots button
            try:
                three_dots_button = post.find_element(By.XPATH, ".//button[contains(@class, 'artdeco-dropdown__trigger') or contains(@class, 'feed-shared-control-menu__trigger')]")
                print(f"Found three-dots menu button using primary selector")
            except:
                try:
                    three_dots_button = post.find_element(By.XPATH, ".//button[.//li-icon[@type='overflow-web-ios']]")
                    print(f"Found three-dots menu button using SVG selector")
                except:
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
            time.sleep(3)
            
            # Find "Copy link to post" option
            print(f"Looking for 'Copy link to post' option...")
            try:
                copy_link_option = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'artdeco-dropdown__content')]//li[contains(., 'Copy link to post') or contains(., 'Copy link')]"))
                )
                print(f"Found 'Copy link to post' option by text content")
            except:
                try:
                    copy_link_option = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'artdeco-dropdown__content')]//li[@aria-label='Copy link to post']"))
                    )
                    print(f"Found 'Copy link to post' option by aria-label")
                except:
                    print(f"Trying to find 'Copy link' by menu position...")
                    time.sleep(2)
                    menu_options = driver.find_elements(By.XPATH, "//div[contains(@class, 'artdeco-dropdown__content')]//li")
                    print(f"Found {len(menu_options)} menu options")
                    
                    if len(menu_options) >= 2:
                        copy_link_option = menu_options[1]
                        print(f"Selected menu item at position 2")
                    else:
                        print(f"Not enough menu options found for post {i+1}")
                        continue
            
            # Click the copy link option
            print(f"Clicking 'Copy link to post' option...")
            copy_link_option.click()
            time.sleep(3)
            
            # Get URL from clipboard
            try:
                post_url = pyperclip.paste()
                print(f"Retrieved from clipboard: {post_url}")
                
                if "linkedin.com" in post_url and post_url not in collected_urls:
                    post_links.append(post_url)
                    collected_urls.add(post_url)
                    print(f"Successfully extracted URL for post {i+1}: {post_url}")
                else:
                    if "linkedin.com" not in post_url:
                        print(f"Clipboard content does not contain a LinkedIn URL")
                    else:
                        print(f"Duplicate URL detected, skipping")
            except Exception as e:
                print(f"Error extracting URL for post {i+1}: {e}")
                
            # Close any open dropdown menu by clicking elsewhere
            print(f"Closing dropdown menu...")
            driver.execute_script("document.body.click();")
            time.sleep(3)
                
        except Exception as e:
            print(f"Error processing post {i+1}: {e}")
    
    return post_links

# Create search.txt if it doesn't exist with default terms
search_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "search.txt")
if not os.path.exists(search_file_path):
    print(f"Search file not found, creating default file at {search_file_path}")
    with open(search_file_path, "w") as f:
        f.write("flutter\npython\njava\nreact")
    print("Created search.txt with default terms")

# Read search terms from file
search_terms = read_search_terms(search_file_path)

# Dictionary to store results for each search term
all_results = {}

# Process each search term
for term in search_terms:
    print(f"\n\n==== Processing search term: {term} ====\n")
    
    # Navigate to search results for this term using the exact same URL structure
    try:
        print(f"Navigating to search results for '{term}'...")
        encoded_term = urllib.parse.quote(term)
        search_url = f"https://www.linkedin.com/search/results/content/?keywords={encoded_term}&origin=FACETED_SEARCH&sid=TT5&sortBy=%22date_posted%22"
        driver.get(search_url)
        print(f"Successfully navigated to search results for '{term}'")
        time.sleep(8)
    except Exception as e:
        print(f"Error navigating to search results for '{term}': {e}")
        continue
    
    # Extract links for this search term
    print(f"\nStarting extraction of post links for '{term}'...")
    term_links = extract_post_links(5)  # Extract 5 links per search term
    
    # Store results for this term
    all_results[term] = term_links

# Print final summary for all search terms
print("\n\n===== FINAL SUMMARY - All search terms =====")
total_links = sum(len(links) for links in all_results.values())
print(f"Processed {len(search_terms)} search terms and extracted {total_links} total links")

for term, links in all_results.items():
    print(f"\nSearch term: {term} - {len(links)} links")
    for i, link in enumerate(links):
        print(f"  {i+1}. {link}")

# Save all results to a file
results_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "linkedin_results.txt")
try:
    with open(results_file, "w") as f:
        f.write(f"LinkedIn Search Results - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(search_terms)} search terms, {total_links} links\n\n")
        
        for term, links in all_results.items():
            f.write(f"Search Term: {term} ({len(links)} results)\n")
            for i, link in enumerate(links):
                f.write(f"{i+1}. {link}\n")
            f.write("\n")
    print(f"\nResults saved to {results_file}")
except Exception as e:
    print(f"Error saving results to file: {e}")

# Don't close the browser immediately
input("\nScript complete. Press Enter to close the browser...")
driver.quit()