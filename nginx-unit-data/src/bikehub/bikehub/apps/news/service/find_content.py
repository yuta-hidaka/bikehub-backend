import requests
from bs4 import BeautifulSoup
from news.models import ContentTag


class FindContents:
    def find_contents(self, url, content_tag, content_tags_class, content_tags_id):
        try:
            res = requests.get(url)
        except Exception as e:
            print(f'This exception happen from find contents request \n {e}')
            return ''

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

    def find_contents_by_tags(self, url: str) -> str:
        tags = ContentTag.objects.all()
        for tag in tags:
            content_text = self.find_contents(
                url,
                tag.tag_type,
                tag.tag_class_name,
                tag.tag_id_name
            )

            if content_text:
                return content_text
