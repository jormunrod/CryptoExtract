from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import now

from core.utils import get_last_updated
from .utils import format_large_number
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
    last_updated = get_last_updated()

    try:
        ix = create_or_open_index(index_dir)
        with ix.searcher() as searcher:
            for doc in searcher.all_stored_fields():
                all_data.append(
                    {
                        'name': doc['name'],
                        'price': f"${float(doc['price']):,.2f}",
                        'change': f"${float(doc['change']):,.2f}",
                        'percent_change': f"{float(doc['percent_change']):.2f}%",
                        'market_cap': format_large_number(doc['market_cap']),
                        'volume': format_large_number(doc['volume']),
                        'volume_in_currency_24h': format_large_number(doc['volume_in_currency_24h']),
                        'total_volume_all_currencies_24h': format_large_number(doc['total_volume_all_currencies_24h']),
                        'circulating_supply': format_large_number(doc['circulating_supply']),
                        'week_change_percent': f"{float(doc['week_change_percent']):.2f}%",
                    }
                )
    except Exception as e:
        all_data = []
        print(f"Error retrieving data: {e}")

    return render(request, 'scraper/list_all_data.html', {'all_data': all_data, 'last_updated': last_updated})
