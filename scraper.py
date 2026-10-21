
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib import robotparser
import json
import time

BASE_URL = "https://quotes.toscrape.com/"
MAX_PAGES = 3
DELAY = 1.5

HEADERS = {
    "User-Agent": "StudentQuoteScraper/1.0 (educational project)"
}


def check_robots(url):
    """Check whether robots.txt permits scraping the URL."""
    robots_url = urljoin(url, "/robots.txt")
    parser = robotparser.RobotFileParser()
    parser.set_url(robots_url)

    try:
        response = requests.get(
            robots_url, headers=HEADERS, timeout=10
        )
        response.raise_for_status()
        parser.parse(response.text.splitlines())
        return parser.can_fetch(HEADERS["User-Agent"], url)
    except requests.RequestException:
        print("Could not verify robots.txt. Stopping for safety.")
        return False


def fetch_page(url):
    """Fetch a webpage and parse its HTML."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_quotes(soup, page_url):
    """Extract quotes, authors, and tags."""
    quotes = []

    for item in soup.select("div.quote"):
        quote_element = item.select_one("span.text")
        author_element = item.select_one("small.author")

        # Check elements before extracting text.
        if quote_element is None or author_element is None:
            continue

        tags = [
            tag.get_text(strip=True)
            for tag in item.select("div.tags a.tag")
        ]

        quotes.append({
            "quote": quote_element.get_text(strip=True),
            "author": author_element.get_text(strip=True),
            "tags": tags,
            "source": page_url
        })

    return quotes


def save_json(quotes):
    """Save extracted quotes in JSON format."""
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=4, ensure_ascii=False)

    print("Quotes saved to quotes.json")


def save_text(quotes):
    """Save extracted quotes in readable text format."""
    with open("quotes.txt", "w", encoding="utf-8") as file:
        for number, item in enumerate(quotes, start=1):
            file.write(f"{number}. {item['quote']}\n")
            file.write(f"   Author: {item['author']}\n")
            file.write(f"   Tags: {', '.join(item['tags'])}\n\n")

    print("Quotes saved to quotes.txt")


def main():
    print("===== QUOTE WEB SCRAPER =====")

    if not check_robots(BASE_URL):
        print("Scraping is not permitted or could not be verified.")
        return

    all_quotes = []
    next_url = BASE_URL
    visited_urls = set()

    for page_number in range(MAX_PAGES):
        if not next_url or next_url in visited_urls:
            break

        if not check_robots(next_url):
            print("Page is not permitted. Stopping.")
            break

        visited_urls.add(next_url)

        try:
            print(f"Fetching page {page_number + 1}...")
            soup = fetch_page(next_url)

            quotes = extract_quotes(soup, next_url)
            all_quotes.extend(quotes)

            next_button = soup.select_one("li.next a")

            if next_button is None:
                break

            next_url = urljoin(next_url, next_button["href"])

            if page_number + 1 < MAX_PAGES:
                time.sleep(DELAY)

        except requests.RequestException as error:
            print("Request failed:", error)
            break

    if not all_quotes:
        print("No quotes collected. Check the connection or page structure.")
        return

    save_json(all_quotes)
    save_text(all_quotes)

    print(f"\nTotal quotes collected: {len(all_quotes)}")
    print("\nFirst quote:")
    print(all_quotes[0]["quote"])
    print("Author:", all_quotes[0]["author"])


if __name__ == "__main__":
    main()
