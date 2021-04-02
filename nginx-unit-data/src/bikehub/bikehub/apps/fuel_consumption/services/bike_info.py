import os
from time import sleep

import requests
from bikehub.modules.scraping.selenium import Selenium
from bs4 import BeautifulSoup
from fuel_consumption.models import Bike, Maker


BASE_URL = 'https://moto.webike.net'


class BikeInfo():
    def __init__(self):
        self.driver = Selenium().get_chrome_driver()
        pass

    def register_bike_info(self) -> set:
        maker_url = "maker/"
        className = "makersearchbox"
        # print()
        try:
            page = requests.get(f'{BASE_URL}/{maker_url}')
        except Exception as e:
            print(f'This exception happen from find contents request \n {e}')
            return ''

        html = BeautifulSoup(page.text, 'lxml')

        a_tags = html.find('div', {'class': className}).findAll('a')

        try:
            for a_tag in a_tags:
                maker_link = a_tag.get('href')
                maker_name = a_tag.contents[0].split('\n')[0].strip()
                bike_info = self.get_bike_info_by_maker_uri(maker_link, maker_name)
                del bike_info
        finally:
            self.driver.close()
            self.driver.quit()
            os.system("pkill chrome")

        print("done")

    def get_bike_info_by_maker_uri(self, maker_link, maker_name):
        cnt = Maker.objects.filter(maker_name_jp__contains=maker_name).count()
        sleep(5)
        if cnt != 1:
            print(maker_name)
        try:
            self.driver.get(f'{BASE_URL}{maker_link}')
            sleep(5)
        except Exception as e:
            print(f'This exception happen from find contents request \n {e}')
            return ()

        btn_view_more_list = self.driver.find_elements_by_class_name('btnViewMore')

        for btn in btn_view_more_list:
            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
            sleep(3)
            self.driver.execute_script("arguments[0].click();", btn)

        html = BeautifulSoup(self.driver.page_source, 'lxml')

        # search_brand_node = html.find('div', {'id': 'search_brand'})

        bikes_by_displacement = html.findAll('div', {'class': 'motoset'})

        for bikes in bikes_by_displacement:
            no_bikes = bikes.findAll('span', {'class': 'no_bike'})
            bike_a_tags = bikes.findAll('a')
            bike_name_list = []

            bike_name_list.extend([
                no_bike.text.replace('(0台)', '') for no_bike in no_bikes
            ])

            bike_name_list.extend([
                bike_a_tag.contents[1].get('alt').strip() for bike_a_tag in bike_a_tags
                if maker_link in bike_a_tag.get('href') and
                bike_a_tag.contents[1].get('alt') and
                ('noimage', 'その他') not in bike_a_tag.contents[1].get('alt')
            ])

        unique_bike_name_list = set(bike_name_list)

        print(unique_bike_name_list)
