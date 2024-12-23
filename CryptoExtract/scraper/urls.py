from django.urls import path
from . import views

urlpatterns = [
    path('load-data/', views.load_data, name='load_data'),
]
