from django.shortcuts import render, redirect
from django.utils.timezone import now

from .utils import scrape_and_index

LAST_UPDATED_FILE = "last_updated.txt"

def load_data(request):
    try:
        scrape_and_index()
        # Guardar la fecha de la última actualización
        with open(LAST_UPDATED_FILE, "w") as f:
            f.write(now().strftime("%Y-%m-%d %H:%M:%S"))
        message = "Data loaded successfully!"
    except Exception as e:
        message = f"Error loading data: {e}"

    return redirect('home')
