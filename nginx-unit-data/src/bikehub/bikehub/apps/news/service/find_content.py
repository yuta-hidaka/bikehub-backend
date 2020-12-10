import requests
from bs4 import BeautifulSoup


class FindContents:
    def find_contents(self, url, content_tag, content_tags_class, content_tags_id):
        print("find context")
        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            return ''

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
