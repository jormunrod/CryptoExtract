from django.urls import path
from . import views

urlpatterns = [
    path('load-data/', views.load_data, name='load_data'),
    path('all-data/', views.list_all_data, name='list_all_data'),
    path('search/', views.search_cryptos, name='search_cryptos'),
    path('top-5-change/', views.top_5_crypto_by_change, name='top_5_crypto_by_change'),
    path('filter-by-price/', views.filter_by_price, name='filter_by_price'),
    path('market-cap-distribution/', views.market_cap_distribution, name='market_cap_distribution'),

]
