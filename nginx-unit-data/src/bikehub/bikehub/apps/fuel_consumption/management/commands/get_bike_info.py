from django.core.management.base import BaseCommand
from fuel_consumption.services.bike_info import BikeInfo

BASE_URL = 'https://moto.webike.net'


class Command(BaseCommand):
    def handle(self, **options):
        bike_info = BikeInfo()
        bike_info.register_bike_info()
