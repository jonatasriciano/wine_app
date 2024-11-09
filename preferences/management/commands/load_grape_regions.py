# preferences/management/commands/load_grape_regions.py

from django.core.management.base import BaseCommand
from preferences.models import GrapeRegion

GRAPE_REGIONS = [
    {"name": "Bordeaux", "country": "France", "famous_for": "Red blends, Cabernet Sauvignon, Merlot", "availability": "High"},
    {"name": "Tuscany", "country": "Italy", "famous_for": "Sangiovese, Chianti, Super Tuscans", "availability": "High"},
    {"name": "Napa Valley", "country": "United States", "famous_for": "Cabernet Sauvignon, Chardonnay", "availability": "High"},
    {"name": "Rioja", "country": "Spain", "famous_for": "Tempranillo, Garnacha", "availability": "High"},
    {"name": "Barossa Valley", "country": "Australia", "famous_for": "Shiraz, GSM blends", "availability": "High"},
    {"name": "Mosel", "country": "Germany", "famous_for": "Riesling", "availability": "High"},
    {"name": "Douro Valley", "country": "Portugal", "famous_for": "Port wine, Touriga Nacional", "availability": "High"},
    {"name": "Marlborough", "country": "New Zealand", "famous_for": "Sauvignon Blanc", "availability": "High"},
    {"name": "Mendoza", "country": "Argentina", "famous_for": "Malbec", "availability": "High"},
    {"name": "Stellenbosch", "country": "South Africa", "famous_for": "Cabernet Sauvignon, Chenin Blanc, Pinotage", "availability": "High"},
]

class Command(BaseCommand):
    help = "Load grape regions into the database"

    def handle(self, *args, **options):
        for region in GRAPE_REGIONS:
            GrapeRegion.objects.get_or_create(
                name=region["name"],
                defaults={
                    "country": region["country"],
                    "famous_for": region["famous_for"],
                    "availability": region["availability"],
                }
            )
        self.stdout.write(self.style.SUCCESS("Grape regions loaded successfully"))