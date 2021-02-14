from django.core.management.base import BaseCommand

from ...service.collect_news import CollectNews
from news.models import News

from django.core.paginator import Paginator


class Command(BaseCommand):
    def handle(self, **options):
        collect_news = CollectNews()

        paginator = Paginator(News.objects.all(), 1000)

        count = 0
        for page_idx in range(1, paginator.num_pages):
            for row in paginator.page(page_idx).object_list:
                count += 1
                collect_news.create_tag(row.summary + ' ' + row.title, row)
            
            print("done")
            print(count)
