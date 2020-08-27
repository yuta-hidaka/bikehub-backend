import requests
from bs4 import BeautifulSoup


class FindImg:
    def find_img(self, entrie, feeds, page_url, target_url):
        img = None
        if 'summary' in entrie and '<img' in entrie['summary']:
            img = self.find_img_general(
                entrie['summary']
            )
        elif 'content' in entrie and '<img' in entrie['content'][0]['value']:
            img = self.find_img_general(
                entrie['content'][0]['value']
            )
        elif 'headlines.yahoo.co.jp' in str(target_url):
            img = self.find_img_from_yahoo(
                page_url
            )
        elif 'feed' in feeds and 'wordpress' in feeds['feed']['generator']:
            img = self.find_img_from_wordpress(
                page_url
            )
        return img

    @staticmethod
    def find_img_general(_html):
        src = False
        html = BeautifulSoup(_html, 'lxml')
        result = html.find('img')
        if result:
            src = result.get('src').split('?')[0]

        return src

    @staticmethod
    def find_img_from_yahoo(url):
        src = False
        res = requests.get(url)
        res.raise_for_status()

        html = BeautifulSoup(res.text, 'lxml')
        pic = html.find('picture')

        if pic:
            src = pic.img.get('src').split('?')[0]

        return src

    @staticmethod
    def find_img_from_wordpress(url):
        src = False
        res = requests.get(url)
        res.raise_for_status()

        html = BeautifulSoup(res.text, 'lxml')
        pic = html.select('img[class*="wp-image-"]')

        if pic:
            src = pic[0].get('src').split('?')[0]

        return src
