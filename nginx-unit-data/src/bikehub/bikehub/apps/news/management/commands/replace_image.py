import pathlib
from concurrent.futures import ThreadPoolExecutor

from common_modules.service.image.image import get_remote_image
from django.core.files import File
from django.core.management.base import BaseCommand
from news.models import News


class Command(BaseCommand):
    def handle(self, **options):
        news_list = News.objects.all().order_by('-created_at')

        print(len(news_list))
        # for news in news_list:
        with ThreadPoolExecutor(max_workers=10, thread_name_prefix="thread") as executor:
            executor.map(self.replace_img, news_list)

        print("done")

    @staticmethod
    def replace_img(news):
        if news.featured_image:
            try:
                tmp_img = get_remote_image(news.featured_image)
                if tmp_img:
                    extension = pathlib.Path(news.featured_image).suffix
                    news.owned_featured_image.save(
                        f"featured_image_{news.pk}{extension}",
                        File(tmp_img)
                    )
                    news.thumbnail_image.save(
                        f"thumbnail_image_{news.pk}{extension}",
                        File(tmp_img)
                    )
                    img = news.owned_featured_image
                    news.featured_image = f'https://dlnqgsc0jr0k.cloudfront.net/{img}'
                else:
                    news.featured_image = ''
            except Exception:
                news.featured_image = ''

            news.save()
