from django.core.management.base import BaseCommand
from football.utils import fetch_and_create

class Command(BaseCommand):
    help = 'Fetch data from API and create objects'

    def handle(self, *args, **options):
        fetch_and_create()
