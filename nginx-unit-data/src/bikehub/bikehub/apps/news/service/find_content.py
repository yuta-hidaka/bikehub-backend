import requests
from bs4 import BeautifulSoup
from news.models import *


class FindContents:
    def find_contents(self, url, content_tag, content_tags_class, content_tags_id):

        res = requests.get(url)
        if not res:
            return ''

        html = BeautifulSoup(res.text, 'lxml')

        if content_tags_id:
            text = html.find(content_tag, {'id': content_tags_id})
        elif content_tags_class:
            text = html.find(content_tag, {'class': content_tags_class})
        else:
            text = html.find(content_tag)

        if text:
            return text.get_text()
        else:
            return ''
