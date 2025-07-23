import requests
from bs4 import BeautifulSoup
import os
import re
from collections import Counter
import html
import json
import urllib.parse

# Set your API key here (DO NOT share this publicly in real applications)
API_KEY = "AIzaSyCbront9JOSSC3vEa-rBM4rLPx82pg2Kio"

# Create folder to store images
os.makedirs("elpais_images", exist_ok=True)

def translate_text(text, target_lang='en', source_lang='es'):
    """
    Translate text using Google Translate API directly
    """
    url = "https://translation.googleapis.com/language/translate/v2"
    
    params = {
        'q': text,
        'target': target_lang,
        'source': source_lang,
        'key': API_KEY,
        'format': 'text'  # This helps with HTML content
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        result = response.json()
        return result['data']['translations'][0]['translatedText']
    except Exception as e:
        print(f"❌ Translation error: {str(e)}")
        return "[Translation Failed]"

def clean_text(text):
    # Decode HTML entities
    text = html.unescape(text)
    # Remove special characters but keep Spanish characters
    text = re.sub(r'[^\w\s\u00C0-\u017FáéíóúüñÁÉÍÓÚÜÑ,.¿?¡!]+', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

# Fetch the Opinión section
url = "https://elpais.com/opinion/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Get first 5 unique opinion article links
articles = soup.select('article a[href*="/opinion/"]')
unique_links = []
for a in articles:
    href = a.get('href')
    if href and href not in unique_links and len(unique_links) < 5:
        unique_links.append(href)

# Scrape article data
article_data = []

for link in unique_links:
    full_link = "https://elpais.com" + link if link.startswith('/') else link
    res = requests.get(full_link, headers=headers)
    article_soup = BeautifulSoup(res.content, 'html.parser')

    title_tag = article_soup.find('h1')
    content_paragraphs = article_soup.select('div.a_styled-content p')

    if not title_tag:
        continue

    title = title_tag.text.strip()
    content = "\n".join(p.text.strip() for p in content_paragraphs if p.text.strip())

    # Download image if available
    image_tag = article_soup.find("img")
    image_url = image_tag.get("src") if image_tag else None
    image_path = ""

    if image_url and image_url.startswith("http"):
        try:
            safe_title = re.sub(r'\W+', '_', title[:30])
            image_path = os.path.join("elpais_images", f"{safe_title}.jpg")
            img_res = requests.get(image_url)
            with open(image_path, "wb") as f:
                f.write(img_res.content)
            print(f"✅ Image downloaded: {image_path}")
        except Exception as e:
            print(f"❌ Image download failed: {e}")

    article_data.append({
        "title": title,
        "content": content,
        "image_path": image_path
    })

# Translate article titles
translated_titles = []
print("\n🔄 Translating Titles to English:")

for i, article in enumerate(article_data, 1):
    original_title = article["title"]
    
    # Clean and prepare the text for translation
    cleaned_title = clean_text(original_title)
    
    # Translate the text
    translated = translate_text(cleaned_title)
    
    # Clean up the translated text if successful
    if translated != "[Translation Failed]":
        translated = html.unescape(translated)

    translated_titles.append(translated)

    print(f"\n📝 Article {i}")
    print("🇪🇸 Original:", original_title)
    print("🇬🇧 Translated:", translated)
    print("🖼️ Image:", article["image_path"] if article["image_path"] else "No image")

# Analyze repeated words in translated titles
print("\n🔍 Repeated Words in Translated Titles (appeared more than 2 times):")

all_words = []
for title in translated_titles:
    if title != "[Translation Failed]":  # Only analyze successful translations
        words = re.findall(r'\b\w+\b', title.lower())
        all_words.extend(words)

word_counts = Counter(all_words)
repeated_words = {word: count for word, count in word_counts.items() if count > 2}

if repeated_words:
    for word, count in repeated_words.items():
        print(f"📊 {word}: {count} times")
else:
    print("ℹ️ No repeated words found.")
