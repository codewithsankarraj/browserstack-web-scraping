import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import os
import time
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
import html
import json

# Test configurations for 5 parallel threads
BROWSER_CONFIGS = [
    {
        "os": "Windows",
        "os_version": "11",
        "browser": "Chrome",
        "browser_version": "latest",
        "name": "Chrome Windows Test"
    },
    {
        "os": "Windows",
        "os_version": "10",
        "browser": "Firefox",
        "browser_version": "latest",
        "name": "Firefox Windows Test"
    },
    {
        "os": "OS X",
        "os_version": "Monterey",
        "browser": "Safari",
        "browser_version": "15.0",
        "name": "Safari Mac Test"
    },
    {
        "deviceName": "iPhone 14",
        "platformName": "iOS",
        "platformVersion": "16",
        "name": "iOS Mobile Test"
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "platformName": "Android",
        "platformVersion": "12.0",
        "name": "Android Mobile Test"
    }
]

def translate_text(text, source_lang='es', target_lang='en'):
    """Translate text using MyMemory's free translation API"""
    text = clean_text(text)
    url = "https://api.mymemory.translated.net/get"
    params = {'q': text, 'langpair': f"{source_lang}|{target_lang}"}
    
    try:
        time.sleep(1)  # Rate limit respect
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        
        if result['responseStatus'] == 200:
            return html.unescape(result['responseData']['translatedText'])
        return "[Translation Failed]"
    except Exception:
        return "[Translation Failed]"

def clean_text(text):
    """Clean text for translation"""
    text = html.unescape(text)
    text = re.sub(r'[^\w\s\u00C0-\u017FáéíóúüñÁÉÍÓÚÜÑ,.¿?¡!]+', ' ', text)
    return ' '.join(text.split())

def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download image {url}: {str(e)}")
        return False

def print_article_details(article_data, idx):
    """Print article details in a formatted way"""
    print(f"\n{'='*50}")
    print(f"Article {idx}:")
    print(f"{'='*50}")
    print(f"\n🇪🇸 Spanish Title:\n{article_data['title']}")
    print(f"\n🇬🇧 English Title:\n{article_data['translated_title']}")
    print(f"\n📝 Content Preview:\n{article_data['content'][:500]}...")
    if article_data['image_path']:
        print(f"\n🖼️ Image saved: {article_data['image_path']}")
    else:
        print("\n❌ No image available")
    print(f"\n{'='*50}\n")

def get_cookie_button_xpath(platform_type):
    """Get the appropriate XPath based on platform"""
    if platform_type == "ios":
        return "//*[text()='Accept and Continue']"
    elif platform_type == "android":
        return "//*[text()='Aceptar']"
    else:  # desktop browsers (Windows/Mac)
        return "//*[text()='Accept']"

def handle_cookie_consent(driver):
    """Handle cookie consent with verification for all browser variations"""
    print("\n🍪 Handling cookie consent...")
    try:
        # Combined XPath for all text variations
        cookie_xpath = "//*[text()='Aceptar' or text()='Accept' or text()='Accept and Continue']"
        
        # Wait for cookie button and verify it exists
        cookie_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, cookie_xpath))
        )
        
        if cookie_button.is_displayed():
            print(f"✅ Found cookie button with text: '{cookie_button.text}'")
            
            # Take screenshot before clicking
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            driver.save_screenshot(f"cookie_before_{timestamp}.png")
            
            # Click the button
            cookie_button.click()
            time.sleep(2)  # Wait longer to ensure popup is gone
            
            # Take screenshot after clicking
            driver.save_screenshot(f"cookie_after_{timestamp}.png")
            
            # Verify cookie popup is gone by checking if any of the buttons are still visible
            try:
                cookie_button = driver.find_element(By.XPATH, cookie_xpath)
                if not cookie_button.is_displayed():
                    print("✅ Cookie popup closed successfully")
                else:
                    print("⚠️ Cookie popup might still be present")
            except:
                print("✅ Cookie popup closed successfully")
                
            return True
    except Exception as e:
        print(f"⚠️ Cookie consent handling: {str(e)}")
        return False

class TestElPaisParallel:
    def setup_class(self):
        """Setup test class - create directories"""
        self.images_dir = "elpais_images"
        os.makedirs(self.images_dir, exist_ok=True)
        print(f"\n📁 Created images directory: {self.images_dir}")

    @pytest.fixture(params=BROWSER_CONFIGS)
    def driver(self, request):
        """Fixture to create WebDriver instance based on configuration"""
        config = request.param
        USERNAME = os.environ.get('BROWSERSTACK_USERNAME', 'sankarraj_WM2vli')
        ACCESS_KEY = os.environ.get('BROWSERSTACK_ACCESS_KEY', 'uyQxQpeV8k6aD3s18TGL')
        URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

        if "deviceName" in config:
            options = webdriver.ChromeOptions()
            browserstack_options = {
                "userName": USERNAME,
                "accessKey": ACCESS_KEY,
                "deviceName": config["deviceName"],
                "platformName": config["platformName"],
                "platformVersion": config["platformVersion"],
                "projectName": "El Pais Scraper",
                "buildName": f"EP-{time.strftime('%Y%m%d-%H%M%S')}",
                "sessionName": config["name"],
                "debug": True,
                "networkLogs": True,
                "seleniumVersion": "4.0.0"
            }
        else:
            if config["browser"].lower() == "chrome":
                options = webdriver.ChromeOptions()
            elif config["browser"].lower() == "firefox":
                options = webdriver.FirefoxOptions()
            elif config["browser"].lower() == "safari":
                options = webdriver.SafariOptions()
            else:
                raise ValueError(f"Unsupported browser: {config['browser']}")

            browserstack_options = {
                "userName": USERNAME,
                "accessKey": ACCESS_KEY,
                "os": config["os"],
                "osVersion": config["os_version"],
                "browserName": config["browser"],
                "browserVersion": config["browser_version"],
                "projectName": "El Pais Scraper",
                "buildName": f"EP-{time.strftime('%Y%m%d-%H%M%S')}",
                "sessionName": config["name"],
                "local": "false",
                "debug": True,
                "networkLogs": True,
                "seleniumVersion": "4.0.0"
            }

        # Add Spanish language preference
        options.add_argument("--lang=es")
        options.add_argument("--accept-lang=es")
        options.set_capability('bstack:options', browserstack_options)

        try:
            driver = webdriver.Remote(
                command_executor=URL,
                options=options
            )
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            yield driver
            
            try:
                # Mark test status on BrowserStack
                script = 'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status": "passed", "reason": "All tests passed successfully!"}}'
                driver.execute_script(script)
                
                # Get build URL
                build_info = {
                    "automation_build": {
                        "name": browserstack_options["buildName"],
                        "url": f"https://automate.browserstack.com/builds/{browserstack_options['buildName']}"
                    }
                }
                driver.execute_script(f'browserstack_executor: {{"action": "annotate", "arguments": {json.dumps(build_info)}}}')
                
            except Exception as e:
                print(f"Failed to update test status: {str(e)}")
                
        except Exception as e:
            pytest.fail(f"Failed to initialize WebDriver: {str(e)}")
        finally:
            if 'driver' in locals():
                driver.quit()

    def test_elpais_scraper(self, driver):
        """Test El Pais scraping and translation functionality"""
        try:
            print("\n🌐 Starting El País scraper test...")
            
            # Get browser info for logging
            try:
                caps = driver.capabilities
                browser_info = f"{caps.get('browserName', 'unknown')} on {caps.get('platformName', 'unknown')}"
                print(f"🌐 Testing on: {browser_info}")
            except:
                print("⚠️ Could not determine browser info")
            
            # Navigate to El País Opinion section
            print("\n🔍 Accessing El País Opinion section...")
            driver.get("https://elpais.com/opinion/")
            
            # Handle cookie consent on main page
            if not handle_cookie_consent(driver):
                print("⚠️ Continuing without cookie consent...")
            
            # Wait for articles to load
            print("\n⏳ Loading articles...")
            articles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article'))
            )[:5]
            
            print(f"✅ Found {len(articles)} articles")
            
            assert len(articles) > 0, "No articles found"
            
            # Store article data
            article_data = []
            
            # Process each article
            for idx, article in enumerate(articles, 1):
                print(f"\n📄 Processing article {idx} of 5...")
                try:
                    # Get title
                    title_el = article.find_element(By.CSS_SELECTOR, 'h2 a')
                    title = title_el.text.strip()
                    link = title_el.get_attribute('href')
                    
                    print(f"🔗 Article URL: {link}")
                    
                    # Get content by visiting article page
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(link)
                    
                    # Handle cookie consent on article page
                    handle_cookie_consent(driver)
                    
                    # Wait for content to load
                    content_elements = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.a_c p'))
                    )
                    content = "\n".join([el.text.strip() for el in content_elements])
                    
                    # Get image
                    image_path = None
                    try:
                        img_el = driver.find_element(By.CSS_SELECTOR, 'article img')
                        img_url = img_el.get_attribute('src')
                        if img_url:
                            safe_title = re.sub(r'[^\w\s-]', '', title)[:30]
                            image_path = os.path.join(self.images_dir, f"{safe_title}_{idx}.jpg")
                            if download_image(img_url, image_path):
                                print(f"✅ Downloaded image: {image_path}")
                            else:
                                print("❌ Failed to download image")
                    except Exception as e:
                        print(f"⚠️ Image error: {str(e)}")
                    
                    # Close article tab and switch back
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    
                    # Translate title
                    print("🔄 Translating title...")
                    translated_title = translate_text(title)
                    
                    article_data.append({
                        'title': title,
                        'translated_title': translated_title,
                        'content': content,
                        'image_path': image_path
                    })
                    
                    # Print article details
                    print_article_details(article_data[-1], idx)
                    
                except Exception as e:
                    print(f"❌ Error processing article {idx}: {str(e)}")
                    continue
            
            assert len(article_data) > 0, "No articles were successfully processed"
            
            # Analyze repeated words in translated titles
            print("\n📊 Analyzing word frequencies in translated titles...")
            all_words = []
            for article in article_data:
                if article['translated_title'] != "[Translation Failed]":
                    words = re.findall(r'\b\w+\b', article['translated_title'].lower())
                    all_words.extend(words)
            
            word_counts = Counter(all_words)
            repeated_words = {word: count for word, count in word_counts.items() if count > 2}
            
            if repeated_words:
                print("\n🔄 Repeated words (appeared more than twice):")
                for word, count in repeated_words.items():
                    print(f"  • {word}: {count} times")
            else:
                print("\nℹ️ No words repeated more than twice")
            
            # Log results to BrowserStack
            results = {
                'articles': [
                    {
                        'title': art['title'],
                        'translated_title': art['translated_title'],
                        'has_image': bool(art['image_path']),
                        'content_length': len(art['content'])
                    }
                    for art in article_data
                ],
                'repeated_words': repeated_words
            }
            
            try:
                print("\n📤 Sending results to BrowserStack...")
                driver.execute_script(
                    'browserstack_executor: {"action": "annotate", "arguments": {"data": "' + 
                    str(results).replace('"', '\\"') + '"}}'
                )
                print("✅ Results sent successfully")
            except Exception as e:
                print(f"⚠️ Failed to log results to BrowserStack: {str(e)}")
            
        except Exception as e:
            error_msg = f"Test failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status": "failed", "reason": "' + 
                error_msg.replace('"', '\\"') + '"}}'
            )
            pytest.fail(error_msg)
            
        print("\n✅ Test completed successfully!")

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to track test status for BrowserStack reporting"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{call.when}", rep) 