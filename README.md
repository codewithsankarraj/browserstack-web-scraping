# El País Web Scraper and BrowserStack Test

This project contains two main components:
1. A web scraper for El País newspaper articles with translation functionality
2. A BrowserStack integration test script

## Features

### Scraper (scraper_translate.py)
- Scrapes articles from El País opinion section
- Translates article titles from Spanish to English
- Downloads article images
- Analyzes word frequency in translated titles

### BrowserStack Test (browserstack_test.py)
- Tests website functionality using BrowserStack
- Supports cross-browser testing
- Takes screenshots of the testing process

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Scraper
```bash
python scraper_translate.py
```

### Running BrowserStack Tests
```bash
python browserstack_test.py
```

## Project Structure
- `scraper_translate.py`: Main scraping and translation script
- `browserstack_test.py`: BrowserStack integration test
- `requirements.txt`: Python dependencies
- `.gitignore`: Git ignore rules

## Output
- Translated articles are displayed in the console
- Images are saved in `elpais_images/` directory
- Screenshots are saved in `elpais_screenshots/` directory

## Requirements
- Python 3.6+
- See `requirements.txt` for Python package dependencies

## Note
Make sure to update BrowserStack credentials in `browserstack_test.py` before running tests. 
