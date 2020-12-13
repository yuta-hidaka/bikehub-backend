import pathlib

import tweepy
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from news.models import News


class Command(BaseCommand):
    def handle(self, **options):
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        base_url = 'https://web.bikehub.app/article'

        news = News.objects.\
            filter(~Q(featured_image=''), is_posted=False)\
            .order_by('-created_at').first()

        if not news:
            return

        img_url = news.featured_image
        extension = pathlib.Path(img_url).suffix

        if not extension:
            return

        author = news.source_site.name if news.site.is_there_another_source else news.site.name

        message = f'【BikeHubニュース便】 \n - {author} - {news.title}  \n #バイク好きと繋がりたい #バイクのある生活 #バイクのニュース #BikeHub \n'
        url = f'{base_url}/{news.news_id}'

        diff = (len(message) + len(url)) - 140

        if diff > 0:
            title = news.title[:((len(message) + len(url)) - (diff + 5))] + '...'
            message = f'【BikeHubニュース便】 \n - {author} - {title}  \n #バイク好きと繋がりたい #バイクのある生活 #バイクのニュース #BikeHub \n'
            print("too long")
            print(diff)
            print(((len(message) + len(url)) - (diff - 5)))
            print(f'{message}{url}')
            print(len(f'{message}{url}'))

        api.update_status(status=f'{message}{url}')

        news.is_posted = True
        news.save()
