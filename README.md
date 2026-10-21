# Quote Web Scraper

## Project Description
A beginner-friendly Python web scraper that fetches quotes from Quotes to Scrape, extracts quote text, author names, and tags using BeautifulSoup, and saves the results as JSON and plain text.

## Features
- HTTP requests using `requests`
- HTML parsing using BeautifulSoup
- CSS selectors for quote extraction
- JSON and text file output
- Pagination with a page limit
- Network error handling and missing-element checks
- robots.txt checks and a delay between requests

## Requirements
- Python 3.10 or newer
- requests
- beautifulsoup4

## Installation
Run:

`pip install requests beautifulsoup4`

## Usage
Run:

`python scraper.py`

The program creates `quotes.json` and `quotes.txt` in the project folder.

## Data Source and Permission
Source: https://quotes.toscrape.com/

I selected this website because it is intended for practicing web scraping. The program checks robots.txt before fetching pages and stops if permission cannot be verified. Website rules and terms should always be checked before scraping.

## Problem Fixed
Some HTML elements may be missing or change over time. I added checks for missing quote and author elements to prevent errors when extracting text. I also added request timeouts and exception handling.

## Files
- `scraper.py` — scraper code
- `quotes.json` — structured quote records
- `quotes.txt` — readable quote output
- `README.md` — documentation
