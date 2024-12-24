from django.shortcuts import render, redirect
from django.utils.timezone import now

from .utils import scrape_and_index
from .whoosh_utils import create_or_open_index

LAST_UPDATED_FILE = "last_updated.txt"

def load_data(request):
    try:
        scrape_and_index()
        with open(LAST_UPDATED_FILE, "w") as f:
            f.write(now().strftime("%d-%m-%Y %H:%M:%S"))
        message = "Data loaded successfully!"
    except Exception as e:
        message = f"Error loading data: {e}"

    return redirect('home')

def list_all_data(request):
    index_dir = "crypto_index"
    all_data = []

    try:
        ix = create_or_open_index(index_dir)
        with ix.searcher() as searcher:
            for doc in searcher.all_stored_fields():
                all_data.append(
                    {
                        'name': doc['name'],
                        'price': doc['price'],
                        'change': doc['change'],
                        'percent_change': doc['percent_change'],
                        'market_cap': doc['market_cap'],
                        'volume': doc['volume'],
                        'volume_in_currency_24h': doc['volume_in_currency_24h'],
                        'total_volume_all_currencies_24h': doc['total_volume_all_currencies_24h'],
                        'circulating_supply': doc['circulating_supply'],
                        'week_change_percent': doc['week_change_percent'],
                    }
                )
    except Exception as e:
        all_data = []
        print(f"Error retrieving data: {e}")

    return render(request, 'scraper/list_all_data.html', {'all_data': all_data})


