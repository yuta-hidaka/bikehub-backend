
import facebook
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        access_token = settings.FACEBOOK_ACCESS_TOKEN
        graph = facebook.GraphAPI(access_token=access_token)
        graph.put_object(
            parent_object='me',
            connection_name='feed',
            message='test2',
            link='https://image.itmedia.co.jp/news/articles/1411/19/yu_group1.jpg'
        )
