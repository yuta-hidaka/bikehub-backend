from concurrent.futures import ThreadPoolExecutor

from django.core.management.base import BaseCommand
from news.models import News
from news.service.find_img import FindImg


class Command(BaseCommand):
    def handle(self, **options):
        self.fi = FindImg()
        news_list = News.objects.all().order_by('-created_at')

        print(len(news_list))
        # for news in news_list:
        with ThreadPoolExecutor(max_workers=1, thread_name_prefix="thread") as executor:
            executor.map(self.replace_img, news_list)

        print("done")

    def replace_img(self, news):
        if news.featured_image.startswith('https://dlnqgsc0jr0k.cloudfront.net'):
            try:

                featured_image = self.fi.find_img(news.url)

                news.featured_image = featured_image
            except Exception as e:
                print(e)
                news.featured_image = ''
        else:
            news.featured_image = ''

        news.save()
