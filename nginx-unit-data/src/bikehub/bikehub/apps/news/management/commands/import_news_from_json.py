import json
from django.db.models import Q
from django.core.management.base import BaseCommand
from news.models import News, SourseSite, TargetSite
from urllib.parse import urlparse

class Command(BaseCommand):
    def find_site(self, data):
        url = urlparse(data['url'])
        site = TargetSite.objects.filter(
            Q(pk=data['site_id']) |
            Q(rss_url__contains=url.netloc) |
            Q(url__contains=url.netloc)
        ).first()

        if site:
            return site
        
        return TargetSite.objects.filter(
            Q(rss_url__contains="news.google.com") |
            Q(url__contains="news.google.com") |
            Q(rss_url__contains="www.youtube.com") |
            Q(url__contains="www.youtube.com")
        ).first()


    def find_source_site(self, target_id):
        return SourseSite.objects.filter(pk=target_id).first()

    def handle(self, **options):
        json_data = open('/code/bikehub/bikehub/apps/news/news.json')
        data = json.load(json_data)

        print(f'length is {len(data[2]["data"])}')

        no = 0
        yes = 0
        for news in data[2]['data']:
            source_site = self.find_source_site(news['source_site_id'])
            site = self.find_site(news)

            if not site:
                print(f"not contain {news['url']}")
                print(f"not contain {news['title']}")
                raise RuntimeError(f"site not exsist")

            if not source_site and not site:
                print(f"not contain {news['url']}")
                print(f"not contain {news['title']}")
                raise RuntimeError(f"source_site not exsist")

            if not site:
                no += 1
            else:
                yes += 1
            print(news['title'])
            exists = News.objects.filter(
                pk=news['news_id'],
            ).exists()

            if not exists:
                print("INSERT")
                obj, created = News.objects.get_or_create(
                    pk=news['news_id'],
                    title=news['title'],
                    summary=news['summary'],
                    url=news['url'],
                    video_id=news['video_id'],

                    # need check
                    site=site,
                    # need check
                    source_site=source_site,

                    featured_image=news['featured_image'],
                    owned_featured_image=news['owned_featured_image'],
                    thumbnail_image=news['thumbnail_image'],
                    is_posted=news['is_posted'],
                    is_youtube=news['is_youtube'],
                    show=news['show'],
                    created_at=news['created_at'],
                    updated_at=news['updated_at'],
                )

        json_data.close()
        print(yes)
        print(no)
