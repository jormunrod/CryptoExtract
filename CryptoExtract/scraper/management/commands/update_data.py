from django.core.management.base import BaseCommand
from scraper.utils import scrape_and_index

class Command(BaseCommand):
    help = 'Fetch and update cryptocurrency data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching and indexing cryptocurrency data...")
        try:
            scrape_and_index()
            self.stdout.write(self.style.SUCCESS("Successfully updated cryptocurrency data!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
