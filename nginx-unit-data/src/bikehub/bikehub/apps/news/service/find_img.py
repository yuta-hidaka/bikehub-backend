import requests
from bs4 import BeautifulSoup


class FindImg:
    def find_img(self, entrie, feeds, page_url, target_url):
        img = None

        if target_url == 'https://kininarubikenews.com/feed' and img is None:
            img = self.find_img_kininaru_baiku_no_news(
                page_url
            )

        if target_url == 'https://response.jp/rss/index.rdf' and img is None:
            img = self.find_img_kininaru_baiku_no_news(
                page_url
            )

        if 'headlines.yahoo.co.jp' in str(target_url) and img is None:
            img = self.find_img_from_yahoo(
                page_url
            )

        img_node = entrie.get('summary', '')
        if 'summary' in entrie and '<img' in img_node and img is None:
            img = self.find_img_general(
                entrie['summary']
            )

        img_node = feeds.get('feed', '')
        img_node = img_node.get('generator', '')
        if 'feed' in feeds and 'wordpress' in img_node and img is None:
            img = self.find_img_from_wordpress(
                page_url
            )

        try:
            img_node = entrie['content'][0]['value']
        except:
            img_node = ''

        if 'content' in entrie and '<img' in img_node and img is None:
            img = self.find_img_general(
                entrie['content'][0]['value']
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
    def find_img_response(url):
        src = False
        res = requests.get(url)
        res.raise_for_status()
        html = BeautifulSoup(res.text, 'lxml')
        result = html.find(
            'div', {'class': 'figure-area'}
        )
        result = html.find(
            'figure', {'class': 'figure'}
        )
        if result:
            result = result.find('img')
            return result.get('src').split('?')[0]
        else:
            return None

    @staticmethod
    def find_img_kininaru_baiku_no_news(url):
        res = requests.get(url)
        res.raise_for_status()
        html = BeautifulSoup(res.text, 'lxml')
        result = html.find(
            'figure', {'class': 'entry-thumbnail'}
        )
        if result:
            result = result.find('img')
            return result.attrs.get('data-src')
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
