import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from fuel_consumption.models import Bike, Maker

BASE_URL = 'https://moto.webike.net'


class Command(BaseCommand):
    def handle(self, **options):
        maker_url = "maker/"
        className = "makersearchbox"

        try:
            res = requests.get(f'{BASE_URL}/{maker_url}')
        except Exception as e:
            print(f'This exception happen from find contents request \n {e}')
            return ''

        html = BeautifulSoup(res.text, 'lxml')

        a_tags = html.find('div', {'class': className}).findAll('a')

        for a_tag in a_tags:
            maker_link = a_tag.get('href')
            maker_name = a_tag.contents[0].split('\n')[0]
            self._get_bike(maker_link, maker_name)
            pass

    @staticmethod
    def _get_bike(maker_link, maker_name):
        cnt = Maker.objects.filter(maker_name_jp__contains=maker_name).count()
        if cnt != 1:
            print(maker_name)
        try:
            res = requests.get(f'{BASE_URL}{maker_link}')
        except Exception as e:
            print(f'This exception happen from find contents request \n {e}')
            return ''
        html = BeautifulSoup(res.text, 'lxml')
        search_brand_node = html.find('div', {'id': 'search_brand'})

        no_bikes = search_brand_node.findAll('span', {'class': 'no_bike'})
        bike_a_tags = search_brand_node.findAll('a')
        bike_name_list = []

        bike_name_list.extend([
            no_bike.text.replace(' (0台)', '') for no_bike in no_bikes
        ])
        bike_name_list.extend([
            bike_a_tag.contents[1].get('alt') for bike_a_tag in bike_a_tags if bike_a_tag.contents[1].get('alt')
        ])

        unique_bike_name_list = set(bike_name_list)

        print(unique_bike_name_list)

        # bike_node =

        # id
        # id search_brand
        # id h2-(*) 01001_99999
