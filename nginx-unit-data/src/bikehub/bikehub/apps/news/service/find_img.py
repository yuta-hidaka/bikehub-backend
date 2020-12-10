import requests
from bs4 import BeautifulSoup


class FindImg:
    def find_img(self, entrie, feeds, page_url, target_url):
        print("find img")
        img = None

        if 'kininarubikenews.com' in page_url and img is None:
            img = self.find_img_kininaru_baiku_no_news(
                page_url
            )

        if 'response.jp' in page_url and img is None:
            img = self.find_img_kininaru_baiku_no_news(
                page_url
            )

        if 'headlines.yahoo.co.jp' in page_url and img is None:
            img = self.find_img_from_yahoo(
                page_url
            )

        img_node = entrie.get('summary', '')
        if 'summary' in entrie and '<img' in img_node and img is None:
            img = self.find_img_by_html(
                entrie['summary']
            )

        img_node = feeds.get('feed', '')
        img_node = img_node.get('generator', '')
        if 'feed' in feeds and 'wordpress' in img_node and img is None:
            img = self.find_img_from_wordpress(
                page_url
            )

        if img is None:
            img = self.find_img_by_url(page_url)

        return img

    @staticmethod
    def find_img_by_url(url):
        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            return None

        if not res:
            return None

        html = BeautifulSoup(res.text, 'lxml')
        images = html.find_all('img')
        if images:
            for image in images:
                src = ''
                if image.get('src'):
                    src = image.get('src').split('?')[0]
                elif image.get('data-src'):
                    src = image.get('data-src').split('?')[0]
                if src.endswith('.jpg') and 'banner' not in src:
                    return src

        else:
            return None

    @staticmethod
    def find_img_by_html(html):
        html = BeautifulSoup(html, 'lxml')
        images = html.find_all('img')
        if images:
            for image in images:
                src = ''
                if image.get('src'):
                    src = image.get('src').split('?')[0]
                elif image.get('data-src'):
                    src = image.get('data-src').split('?')[0]
                if src.endswith('.jpg') and 'banner' not in src:
                    return src

        else:
            return None

    @staticmethod
    def find_img_response(url):
        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            return None
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
        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            return None

        res = requests.get(url)
        if not res:
            return None
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
        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            return None

        res = requests.get(url)
        if not res:
            return None

        html = BeautifulSoup(res.text, 'lxml')
        pic = html.find('picture')

        if pic and pic.img.get('src'):
            return pic.img.get('src').split('?')[0]
        else:
            return None

    @staticmethod
    def find_img_from_wordpress(url):
        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            return None

        res = requests.get(url)
        if not res:
            return None

        html = BeautifulSoup(res.text, 'lxml')
        pic = html.select('img[class*="wp-image-"]')

        if pic and pic[0].get('src'):
            return pic[0].get('src').split('?')[0]
        else:
            return None
