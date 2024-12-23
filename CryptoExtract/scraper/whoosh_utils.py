import os
from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser


# Define the schema
def get_schema():
    return Schema(
        name=TEXT(stored=True),
        price=NUMERIC(stored=True, numtype=float),
        change=NUMERIC(stored=True, numtype=float),
        percent_change=NUMERIC(stored=True, numtype=float),
        market_cap=NUMERIC(stored=True, numtype=float),
        volume=NUMERIC(stored=True, numtype=float),
        volume_in_currency_24h=NUMERIC(stored=True, numtype=float),
        total_volume_all_currencies_24h=NUMERIC(stored=True, numtype=float),
        circulating_supply=NUMERIC(stored=True, numtype=float),
        week_change_percent=NUMERIC(stored=True, numtype=float),
    )


# Create or open the index
def create_or_open_index(index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return index.create_in(index_dir, schema=get_schema())
    return index.open_dir(index_dir)


# Auxiliar function to parse numeric values
def parse_numeric(value):
    try:
        if not value or value == '-':
            return 0.0
        value = value.replace(',', '')
        if value.endswith('T'):
            return float(value[:-1]) * 1_000_000_000_000
        elif value.endswith('B'):
            return float(value[:-1]) * 1_000_000_000
        elif value.endswith('M'):
            return float(value[:-1]) * 1_000_000
        return float(value)
    except (ValueError, AttributeError):
        return 0.0


# Add data to the index
def add_to_index(index_dir, crypto_data):
    ix = create_or_open_index(index_dir)
    writer = ix.writer()

    try:
        for crypto in crypto_data:
            writer.add_document(
                name=crypto['name'],
                price=parse_numeric(crypto['price']),
                change=parse_numeric(crypto['change']),
                percent_change=parse_numeric(crypto['percent_change'].replace('%', '')),
                market_cap=parse_numeric(crypto['market_cap']),
                volume=parse_numeric(crypto['volume']),
                volume_in_currency_24h=parse_numeric(crypto['volume_in_currency_24h']),
                total_volume_all_currencies_24h=parse_numeric(crypto['total_volume_all_currencies_24h']),
                circulating_supply=parse_numeric(crypto['circulating_supply']),
                week_change_percent=parse_numeric(crypto['52_week_change_percent'].replace('%', '')),
            )
        writer.commit()
    except Exception as e:
        writer.cancel()
        raise Exception(f"Failed to add data to index: {e}")


# Search the index
def search_index(index_dir, query_str, field="name"):
    ix = create_or_open_index(index_dir)
    with ix.searcher() as searcher:
        query = QueryParser(field, ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)
        return [
            {
                "name": result["name"],
                "price": result["price"],
                "change": result["change"],
                "percent_change": result["percent_change"],
                "market_cap": result["market_cap"],
                "volume": result["volume"],
                "volume_in_currency_24h": result["volume_in_currency_24h"],
                "total_volume_all_currencies_24h": result["total_volume_all_currencies_24h"],
                "circulating_supply": result["circulating_supply"],
                "week_change_percent": result["week_change_percent"],
            }
            for result in results
        ]
