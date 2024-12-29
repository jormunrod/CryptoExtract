import plotly.express as px
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import now
from whoosh.qparser import QueryParser

from core.utils import get_last_updated
from .utils import format_crypto_data
from .utils import scrape_and_index
from .whoosh_utils import create_or_open_index, search_index

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
                all_data.append(format_crypto_data(doc))
    except Exception as e:
        all_data = []
        print(f"Error retrieving data: {e}")

    return render(request, 'scraper/list_all_data.html', {'all_data': all_data, 'last_updated': last_updated})


def search_cryptos(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        index_dir = "crypto_index"
        try:
            raw_results = search_index(index_dir, query, field="name")
            results = [format_crypto_data(crypto) for crypto in raw_results]
        except Exception as e:
            print(f"Error searching the index: {e}")

    return render(request, 'scraper/search.html', {'query': query, 'results': results})


def top_5_crypto_by_change(request):
    index_dir = "crypto_index"
    top_cryptos = []

    try:
        ix = create_or_open_index(index_dir)
        with ix.searcher() as searcher:
            # Obtener todos los documentos del índice
            results = list(searcher.all_stored_fields())

            # Ordenar por 'percent_change' descendente
            sorted_results = sorted(
                results,
                key=lambda doc: float(doc['percent_change']),
                reverse=True
            )
            top_cryptos = [format_crypto_data(doc) for doc in sorted_results[:5]]

    except Exception as e:
        print(f"Error retrieving data: {e}")

    return render(request, 'scraper/top_5_crypto_by_change.html', {'top_cryptos': top_cryptos})


def filter_by_price(request):
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    filtered_cryptos = []

    if min_price and max_price:
        index_dir = "crypto_index"
        try:
            ix = create_or_open_index(index_dir)
            with ix.searcher() as searcher:
                # Get all documents from the index
                results = list(searcher.all_stored_fields())

                # Filter by price range
                filtered_cryptos = [
                    format_crypto_data(doc) for doc in results
                    if float(min_price) <= float(doc['price']) <= float(max_price)
                ]


        except Exception as e:
            print(f"Error filtering data: {e}")

    return render(request, 'scraper/filter_by_price.html', {'filtered_cryptos': filtered_cryptos})


def market_cap_distribution(request):
    index_dir = "crypto_index"
    crypto_data = []

    try:
        ix = create_or_open_index(index_dir)
        with ix.searcher() as searcher:
            for doc in searcher.all_stored_fields():
                crypto_data.append({
                    'name': doc['name'],
                    'market_cap': float(doc['market_cap']),
                })

        # Order by market cap and get the top 10
        top_cryptos = sorted(crypto_data, key=lambda x: x['market_cap'], reverse=True)[:10]

        # Generate pie chart with the top 10 cryptocurrencies by market cap
        fig = px.pie(
            top_cryptos,
            names='name',
            values='market_cap',
        )
        chart = fig.to_html(full_html=False)

    except Exception as e:
        print(f"Error generating market cap chart: {e}")
        chart = None

    return render(request, 'scraper/market_cap_distribution.html', {'chart': chart})


def compare_cryptos(request):
    selected_cryptos = request.GET.getlist('crypto')
    compared_data = []
    all_names = []

    try:
        index_dir = "crypto_index"
        ix = create_or_open_index(index_dir)
        with ix.searcher() as searcher:
            for doc in searcher.all_stored_fields():
                all_names.append(doc['name'])
                print(f"documetos: {doc}")

            if len(selected_cryptos) == 2:
                print(f"Comparing {selected_cryptos[0]} and {selected_cryptos[1]}")
                for crypto in selected_cryptos:
                    query = QueryParser("name", ix.schema).parse(crypto)
                    results = list(searcher.search(query, limit=1))
                    print(f"Results for {crypto}: {results}")
                    if results:
                        compared_data.append(format_crypto_data(results[0]))
    except Exception as e:
        print(f"Error comparing data: {e}")

    return render(request, 'scraper/compare_cryptos.html', {
        'compared_data': compared_data,
        'selected_cryptos': selected_cryptos,
        'all_names': all_names,
    })
