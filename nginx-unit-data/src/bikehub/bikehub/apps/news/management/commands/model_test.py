import requests
from django.core.management.base import BaseCommand
from news.models import News, MainCategoryTag, SubCategoryTag, SubCategoryTagMap
from django.db.models import Count


class Command(BaseCommand):
    def handle(self, **options):
        # queryset = SubCategoryTagMap.objects\
        # .values('news')\
        # .annotate(news_count=Count('news_id'))

        queryset = SubCategoryTagMap.objects.aggregate(news_count=Count('news_id'))

        print(queryset)

        for q in queryset:
            # print(q.news_count)
            print(q)


