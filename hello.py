from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import os

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")

chromedriver_path = os.path.abspath(r"S:\creuto\chromedriver-win64\chromedriver-win64\chromedriver.exe")
service = Service(executable_path=chromedriver_path)

# Initialize the Chrome driver
try:
    driver = webdriver.Chrome(service=service, options=options)
    print(f"Successfully initialized Chrome driver with path: {chromedriver_path}")
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    exit(1)

# First, navigate to LinkedIn domain
try:
    driver.get("https://www.linkedin.com")
    print("Successfully navigated to LinkedIn homepage")
    time.sleep(5)  # Give more time to load
except Exception as e:
    print(f"Error navigating to LinkedIn: {e}")
    driver.quit()
    exit(1)

try:
    cookies_str = '''lang=v=2&lang=en-us; bcookie="v=2&227038fb-9cc1-4b0c-83a2-fd45c1c3b03d"; bscookie="v=1&20250322164651b721d38a-0d69-412d-8466-cc99b3661d10AQFYdcMcC7-HFO5YawIGYjUvWnzx-bIY"; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; fid=AQGqPjy0fybY4wAAAZW-z-Pfr5zPW0fQN7ptAmzhm5AfWL0o5aPg0QT-lZyI2F6xV5XHtQTs5TqFIg; li_rm=AQH-6JZOb6j9hAAAAZW-1IMvUfZIyiw5ZZLfqdA-qenOIGTAB-XHGA3PXyHK2YBn3af-LVlnQ8sQCC32yXW3FG7L96PcziVd-uKhKk2oFttphgfmORO84uSIzxZo2a7MGPRQwAPcDD4PeQe0cWK3uXHOtgki03Jpn3FypdiAvP44oTXabwiD9-obyv4PKs1cz020FrmtDS6JOoLr_2_6DZojoBN421I93XXuPVS_HvR8dahAt9BjPuuDikd3U-GpTisKWAGMHVQQtzD6Kvl0WSMhjI4OyEosG_TYSBSSS7p-WU9AdVpNfTLQoKbbnNaxhsJa-_rC-R-2SXES5Jk; timezone=Asia/Calcutta; li_theme=light; li_theme_set=app; _gcl_au=1.1.2049496068.1742663411; li_sugr=16779779-3f32-4790-ab09-ac55e9d73529; _guid=676a67b3-aac4-4e7c-a108-bcdb9ad4a276; AnalyticsSyncHistory=AQLVfp44BIAt4wAAAZW-1WD6tB1J35QcN6xVDwmIx2y37HrmZu92-YK0RlT6NWatm1IgT_uU82ZaGnSeaUHxyg; lms_ads=AQGBdkzU7gyLRAAAAZW-1WOxVQdPiepDfHNjoq-gljX4Mv7toUfQpPYn6XibxdNj6hkIPGOvM3U1CImeZf7RQ_Nw8ZMsac5Z; lms_analytics=AQGBdkzU7gyLRAAAAZW-1WOxVQdPiepDfHNjoq-gljX4Mv7toUfQpPYn6XibxdNj6hkIPGOvM3U1CImeZf7RQ_Nw8ZMsac5Z; dfpfpt=b1ad49b3217046a8862fdf122b00057d; fptctx2=taBcrIH61PuCVH7eNCyH0MJojnuUODHcZ6x9WoxhgCmaWz73Cp1vdveOgexqN1AnC%252b11aGi2aSN003DT7u5wITELsRKrePJ%252f1JKZQjxH7JZN7qX%252f0jz%252fCUmflZI%252fpLLITHtbB2fdS1iq2%252bycmqnS0ayApH6BSJc2X2TY4%252bpqn1rJSYoGroavgJHxBtPxy6inPJpPZNKAkg1DGszFr67%252bV5neYWJub5JOye45bcS%252f0%252buvkt1HHsnBkJ8HyXHDxwN9DGvxH5%252fwDB%252fnyvN5XOn%252ffUUiBAo%252bbqxy%252bi9GmgkgWvmpf7c%252f7rqwa1p9Es%252fenNHgEzHKKy1mF42l2DmmxI9VvhqM2hn0cvucanBA6gDpkHQ%253d; li_at=AQEDAVkEwfUAcoWNAAABlb7ZKcUAAAGV4uWtxU0AvJfuc_PzrtRWhauwHQLvO6E-0TG8yjnX6Mh35-q-CRhoxMi0PxwbGNt8NQjJZHwgJm0NzxRHGheN7w6UAQ1wdgXc8xlkixvVXKyk2EuZ9AWp71-M; liap=true; JSESSIONID="ajax:8848163267991900946"; UserMatchHistory=AQKiLQjsan_Q2AAAAZW-4kNmzbYvNEGR1D61EE0T17el9qbqOW32TNo4zUR8ugqAY3fBByc-ypETfTlXCCg9QSI-h_Pc5MOPe6cL7ixapgHTd-8GUs_y3rYtDZSSjvuMVsyZQp4q_-Opg7_AAWji-FcIGLq7lpkyLTHPRAOEsq1zzYm-5O8zfc0yVCkgFzEk7w0MS6MHz0fbvFUht_np6DCcgam9jit2VZ95B9IpvoM0Q22ZLWJRQGwBE5ix_FXHBVebtsmdwsWuZiqRqzVizvb8-Nr57jz-JJQ4AR4ALMQJAyoigAW2h5IMWlDTZ89lgBXRFh0NaT-Hp7_6MZoKeC-QolKn8fBPCxBAeeAZPu3JX0OqhA; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C20170%7CMCMID%7C48212432799623719528993470856891252712%7CMCOPTOUT-1742671456s%7CNONE%7CvVersion%7C5.1.1; lidc="b=VGST09:s=V:r=V:a=V:p=V:g=3142:u=1:x=1:i=1742664255:t=1742749752:v=2:sig=AQG6bCpPKLAA6qFHUil14fEbb9jgIqD_"'''

    cookie_pairs = cookies_str.split('; ')
    added_cookies = 0
    for cookie_pair in cookie_pairs:
        if '=' in cookie_pair:
            name, value = cookie_pair.split('=', 1)
            driver.add_cookie({'name': name, 'value': value, 'domain': '.linkedin.com', 'path': '/'})
            added_cookies += 1
    print(f"Successfully added {added_cookies} cookies")
except Exception as e:
    print(f"Error adding cookies: {e}")

try:
    driver.execute_cdp_cmd('Network.enable', {})
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': headers})
    print("Successfully set headers")
except Exception as e:
    print(f"Error setting headers: {e}")

try:
    driver.get("https://www.linkedin.com/feed/")
    print("Navigated to LinkedIn feed page")
    time.sleep(10)  # Wait longer to see results
except Exception as e:
    print(f"Error navigating to feed: {e}")

# # You can add your scraping logic here
# try:
#     feed_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")
#     print(f"Found {len(feed_items)} posts in feed")
# except Exception as e:
#     print(f"Error finding feed items: {e}")

# Don't close the browser immediately
input("Press Enter to close the browser...")
driver.quit()