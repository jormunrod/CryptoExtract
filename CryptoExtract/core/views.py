from django.shortcuts import render
from .utils import get_last_updated


def home(request):
    last_updated = get_last_updated()
    return render(request, 'core/home.html', {'last_updated': last_updated})


def about(request):
    return render(request, 'core/about.html')


def glossary(request):
    terms = {
        "Cryptocurrency": "A digital or virtual currency that uses cryptography for security and operates independently of a central authority.",
        "Blockchain": "A decentralized and distributed digital ledger that records transactions across multiple computers.",
        "Market Cap": "The total value of a cryptocurrency, calculated by multiplying its current price by the total circulating supply.",
        "Volume": "The total amount of a cryptocurrency that has been traded within a specific time period.",
        "Circulating Supply": "The number of cryptocurrency coins or tokens that are publicly available and circulating in the market.",
        "ICO (Initial Coin Offering)": "A fundraising method where new cryptocurrencies sell tokens to investors.",
        "DeFi (Decentralized Finance)": "A financial ecosystem built on blockchain technology offering services like lending, borrowing, and trading without intermediaries.",
        "Wallet": "A digital tool used to store and manage cryptocurrency assets.",
        "Mining": "The process of validating and adding transactions to a blockchain, typically rewarded with new cryptocurrency tokens.",
        "Proof of Work (PoW)": "A consensus algorithm used to validate transactions and secure a blockchain through computational effort.",
        "Proof of Stake (PoS)": "A consensus algorithm where validators are chosen based on the number of coins they hold and are willing to 'stake' as collateral.",
        "Token": "A type of cryptocurrency that represents an asset or utility and operates on an existing blockchain.",
        "Altcoin": "Any cryptocurrency other than Bitcoin.",
        "Stablecoin": "A type of cryptocurrency that aims to maintain a stable value by being pegged to a reserve asset like the US Dollar.",
        "Decentralization": "The process of distributing and delegating power from a central authority to a network of participants.",
        "Hash Rate": "The measure of computational power used in mining and securing a blockchain.",
    }

    return render(request, 'core/glossary.html', {'terms': terms})