# El País Article Scraper

A Python script that uses Selenium and BrowserStack to scrape articles from El País opinion section.

## Features

- Scrapes article titles, authors, timestamps, and summaries
- Takes screenshots of articles
- Runs tests on BrowserStack's cloud infrastructure
- Supports multiple browser configurations

## Prerequisites

- Python 3.6 or higher
- BrowserStack account and credentials
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Update the BrowserStack credentials in `browserstack_test.py`:
```python
USERNAME = 'your_username'
ACCESS_KEY = 'your_access_key'
```

## Usage

Run the script:
```bash
python browserstack_test.py
```

The script will:
1. Connect to BrowserStack
2. Navigate to El País opinion section
3. Extract article information
4. Take screenshots of articles
5. Save results in the `elpais_screenshots` directory

## Output

- Console output showing article details
- Screenshots saved in `elpais_screenshots` directory
- Each screenshot named with article number and timestamp

## License

This project is licensed under the MIT License - see the LICENSE file for details.
