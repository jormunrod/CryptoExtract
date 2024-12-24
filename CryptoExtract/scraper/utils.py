import os

import requests
from bs4 import BeautifulSoup
from whoosh import index

from .whoosh_utils import add_to_index, get_schema


def fetch_crypto_data():
    url = "https://finance.yahoo.com/markets/crypto/all/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse the data table
    table = soup.find('table', {'class': 'markets-table'})
    if not table:
        raise Exception("Failed to locate the data table on the page")

    rows = table.find_all('tr')[1:]  # Skip the header row
    crypto_data = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 13:
            continue

        try:
            crypto_data.append({
                'name': cols[1].text.strip(),
                'price': cols[3].find('fin-streamer', {'data-field': 'regularMarketPrice'}).text.strip(),
                'change': cols[4].find('fin-streamer', {'data-field': 'regularMarketChange'}).text.strip(),
                'percent_change': cols[5].find('fin-streamer',
                                               {'data-field': 'regularMarketChangePercent'}).text.strip(),
                'market_cap': cols[6].find('fin-streamer', {'data-field': 'marketCap'}).text.strip(),
                'volume': cols[7].find('fin-streamer', {'data-field': 'regularMarketVolume'}).text.strip(),
                'volume_in_currency_24h': cols[8].text.strip(),
                'total_volume_all_currencies_24h': cols[9].text.strip(),
                'circulating_supply': cols[10].text.strip(),
                '52_week_change_percent': cols[11].text.strip(),
            })
        except AttributeError:
            # Skip rows with missing data
            continue

    return crypto_data


def scrape_and_index():
    index_dir = "crypto_index"

    # Recreate the index safely
    if os.path.exists(index_dir):
        for file in os.listdir(index_dir):
            file_path = os.path.join(index_dir, file)
            os.remove(file_path)

    # Create a new index
    ix = index.create_in(index_dir, schema=get_schema())

    try:
        crypto_data = fetch_crypto_data()
        add_to_index(index_dir, crypto_data)
    except Exception as e:
        raise Exception(f"Scraping and indexing failed: {e}")


def format_large_number(value):
    """
    Converts a large number into a human-readable string with suffixes.
    e.g., 1_000_000 -> "1M", 1_000_000_000 -> "1B", 1_000_000_000_000 -> "1T"
    """
    try:
        value = float(value)
        if value >= 1_000_000_000_000:  # Trillions
            return f"{value / 1_000_000_000_000:.2f}T"
        elif value >= 1_000_000_000:  # Billions
            return f"{value / 1_000_000_000:.2f}B"
        elif value >= 1_000_000:  # Millions
            return f"{value / 1_000_000:.2f}M"
        return f"{value:.2f}"  # Smaller numbers
    except (ValueError, TypeError):
        return "N/A"  # Fallback for invalid or missing values
