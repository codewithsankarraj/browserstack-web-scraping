from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import time

print("🟢 Script started.")

try:
    print("Selenium imported successfully.")
except Exception as e:
    print("❌ Error importing Selenium:", e)
    exit()

# BrowserStack credentials
USERNAME = 'sankarraj_WM2vli'
ACCESS_KEY = 'uyQxQpeV8k6aD3s18TGL'

# Remote URL for BrowserStack
URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Create screenshots directory if it doesn't exist
SCREENSHOTS_DIR = "elpais_screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Setup Chrome Options
options = webdriver.ChromeOptions()
options.set_capability('browserName', 'Chrome')
options.set_capability('browserVersion', 'latest')
options.set_capability('bstack:options', {
    'os': 'Windows',
    'osVersion': '10',
    'sessionName': 'El Pais Opinion Scraper Test',
    'buildName': f"EP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
})

print("Launching remote browser on BrowserStack...")

driver = webdriver.Remote(
    command_executor=URL,
    options=options
)

try:
    print("Navigating to El País...")
    driver.get("https://elpais.com/opinion/")

    print("Waiting for articles to load...")
    articles = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
    )

    print(f" Found {len(articles)} articles.\n")

    # Process articles with more details
    for idx, article in enumerate(articles[:5], start=1):
        try:
            print(f"\n📄 Processing Article {idx}")
            print("=" * 50)

            # Extract article details
            title_el = article.find_element(By.CSS_SELECTOR, 'h2 a')
            title = title_el.text.strip()
            link = title_el.get_attribute("href")

            # Try to get author and timestamp
            try:
                author = article.find_element(By.CSS_SELECTOR, '.c_a_n').text.strip()
                print(f"✍️ Author: {author}")
            except:
                print("ℹ️ No author found")

            try:
                timestamp = article.find_element(By.CSS_SELECTOR, 'time').get_attribute("datetime")
                print(f"🕒 Published: {timestamp}")
            except:
                print("ℹ️ No timestamp found")

            # Try to get article summary
            try:
                summary = article.find_element(By.CSS_SELECTOR, '.c_d').text.strip()
                print(f"📝 Summary: {summary}")
            except:
                print("ℹ️ No summary found")

            print(f"📰 Title: {title}")
            print(f"🔗 Link: {link}")

            # Take screenshot of the article
            print("📸 Taking screenshot...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"article_{idx}_{timestamp}.png")
            
            # Scroll article into view for better screenshot
            driver.execute_script("arguments[0].scrollIntoView(true);", article)
            time.sleep(1)  # Wait for scroll animation
            
            # Take screenshot of specific article
            article.screenshot(screenshot_path)
            print(f"✅ Screenshot saved: {screenshot_path}")

        except Exception as e:
            print(f"⚠️ Error processing article {idx}: {e}")

finally:
    driver.quit()
    print("\n✅ Test completed and browser closed.")
