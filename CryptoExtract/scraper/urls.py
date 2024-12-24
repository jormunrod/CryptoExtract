from django.urls import path
from . import views

urlpatterns = [
    path('load-data/', views.load_data, name='load_data'),
    path('all-data/', views.list_all_data, name='list_all_data'),
    path('search/', views.search_cryptos, name='search_cryptos'),

]
