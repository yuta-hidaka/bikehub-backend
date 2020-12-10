import pathlib

from common_modules.service.image.image import get_remote_image
from django.core.files import File
from django.core.management.base import BaseCommand
from news.models import News


class Command(BaseCommand):
    def handle(self, **options):
        news_list = News.objects.all()

        for news in news_list:
            if news.featured_image and not news.owned_featured_image:
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
