import requests
from bs4 import BeautifulSoup
import logging
import argparse
from urllib.parse import urljoin, urlparse


def scrape_licensed_character_links(url):
    try:
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Validate URL
        if not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL. Please include 'http://' or 'https://'.")

        # Send a GET request to the URL
        logging.info(f"Fetching URL: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all licensed character links and convert to absolute URLs
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        licensed_character_links = soup.find_all('a', href=True)

        # Filter and normalize links
        unique_links = set()
        for link in licensed_character_links:
            # Convert relative URLs to absolute
            full_url = urljoin(base_url, link['href'])

            # Optional: Add additional filtering criteria
            if full_url.startswith(base_url):
                unique_links.add(full_url)

        # Sort links
        sorted_links = sorted(unique_links)

        # Save links to a text file
        output_file = 'licensed_character_links.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for link in sorted_links:
                f.write(link + '\n')

        logging.info(f"Successfully saved {len(sorted_links)} unique licensed character links to {output_file}")
        return sorted_links

    except requests.RequestException as e:
        logging.error(f"Error fetching the webpage: {e}")
        return []
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Scrape licensed character links from a given URL')
    parser.add_argument('url', type=str, help='URL to scrape licensed character links from')
    parser.add_argument('-o', '--output', type=str, default='licensed_character_links.txt',
                        help='Output file name (default: licensed_character_links.txt)')

    # Parse arguments
    args = parser.parse_args()

    # Scrape links
    scraped_links = scrape_licensed_character_links(args.url)

    # Print links to console
    for link in scraped_links:
        print(link)


if __name__ == "__main__":
    main()