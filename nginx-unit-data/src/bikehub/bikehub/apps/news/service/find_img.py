import requests
from bs4 import BeautifulSoup


class FindImg:
    def find_img(self, entrie, feeds, page_url, target_url):
        img = None

        if target_url == 'https://kininarubikenews.com/feed':
            self.find_img_kininaru_baiku_no_news(
                page_url
            )
            pass
        elif 'summary' in entrie and '<img' in entrie['summary']:
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
            return result.get('src').split('?')[0]
        else:
            return None

    @staticmethod
    def find_img_kininaru_baiku_no_news(url):
        src = False
        html = BeautifulSoup(url, 'lxml')
        result = html.find(
            'figure', {'class': 'entry-thumbnail'}
        )
        if result:
            result = result.find('img')
            return result.get('src').split('?')[0]
        else:
            return None

    @staticmethod
    def find_img_from_yahoo(url):
        src = False
        res = requests.get(url)
        res.raise_for_status()

        html = BeautifulSoup(res.text, 'lxml')
        pic = html.find('picture')

        if pic:
            return pic.img.get('src').split('?')[0]
        else:
            return None

    @staticmethod
    def find_img_from_wordpress(url):
        src = False
        res = requests.get(url)
        res.raise_for_status()

        html = BeautifulSoup(res.text, 'lxml')
        pic = html.select('img[class*="wp-image-"]')

        if pic:
            return pic[0].get('src').split('?')[0]
        else:
            return None
