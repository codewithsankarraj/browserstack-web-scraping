# El País Article Scraper with BrowserStack Testing

This project scrapes articles from El País newspaper's opinion section and tests the functionality across multiple browsers using BrowserStack.

## Features

1. **Article Scraping**
   - Visits El País Spanish website
   - Scrapes first 5 articles from the Opinion section
   - Extracts titles and full content in Spanish
   - Downloads article cover images

2. **Translation**
   - Translates article titles to English
   - Uses MyMemory Translation API
   - Preserves Spanish characters and formatting

3. **Analysis**
   - Identifies repeated words in translated titles
   - Reports word frequency statistics
   - Validates Spanish content

4. **Cross-Browser Testing**
   - Tests on 5 different platforms in parallel:
     - Windows 11 + Chrome (latest)
     - Windows 10 + Firefox (latest)
     - macOS Monterey + Safari 15
     - iOS (iPhone 14)
     - Android (Samsung Galaxy S22)

## Project Structure

```
.
├── browserstack_parallel_test.py   # Main test script
├── requirements.txt                # Python dependencies
├── elpais_images/                 # Downloaded article images
└── README.md                      # Project documentation
```

## Setup

1. **Environment Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **BrowserStack Configuration**
   ```bash
   # Set BrowserStack credentials
   export BROWSERSTACK_USERNAME='your_username'
   export BROWSERSTACK_ACCESS_KEY='your_access_key'
   ```

## Running Tests

Run tests in parallel across all platforms:
```bash
pytest browserstack_parallel_test.py -v -n 5
```

## Test Flow

1. **Browser Setup**
   - Initializes each browser with Spanish language preferences
   - Configures BrowserStack capabilities
   - Sets up debugging and network logging

2. **Content Scraping**
   - Visits El País opinion section
   - Identifies first 5 articles
   - Extracts titles and content
   - Downloads article images

3. **Translation & Analysis**
   - Translates article titles to English
   - Analyzes word frequency
   - Reports repeated words

4. **Validation & Reporting**
   - Verifies Spanish content
   - Validates article structure
   - Reports results to BrowserStack dashboard

## Requirements

- Python 3.8+
- BrowserStack account
- Internet connection
- Required Python packages (see requirements.txt)

## Notes

- Image downloads are stored in `elpais_images/` directory
- Test results are available in BrowserStack dashboard
- Network logs and screenshots are captured for debugging
- Tests run in parallel to optimize execution time 
