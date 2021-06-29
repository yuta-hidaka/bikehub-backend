import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        url = 'http://133.167.102.92:8888/rest/news/'
        headers = {'Authorization': 'Api-Key hnIVbuI3.4zBiAyiOWFR5abnm26JcBCQ2Niqa6QCu'}

        x = requests.get(url, headers=headers)

        print(x.text)