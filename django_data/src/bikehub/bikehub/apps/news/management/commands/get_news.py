from django.core.management.base import BaseCommand
import feedparser
import json


class Command(BaseCommand):
    def handle(self, **options):
        listData = [
            'https://headlines.yahoo.co.jp/rss/autoby-all.xml',
            'https://news.yahoo.co.jp/pickup/rss.xml',
        ]

        for l in listData:
            d = feedparser.parse(l)
            print(print(json.dumps(d, indent=2, ensure_ascii=False)))

        print('FROM GET_NEWS')

        # 必要なkey
        # 
