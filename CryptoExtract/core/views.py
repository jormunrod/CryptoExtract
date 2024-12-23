from django.shortcuts import render
from .utils import get_last_updated


def home(request):
    last_updated = get_last_updated()
    return render(request, 'core/home.html', {'last_updated': last_updated})


def about(request):
    return render(request, 'core/about.html')
