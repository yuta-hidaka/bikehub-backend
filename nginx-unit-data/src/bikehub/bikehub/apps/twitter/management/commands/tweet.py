import os
import pathlib

import requests
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

        message = f'【BikeHubニュース便】 \n - {author} - {news.title}  \n #バイク好きと繋がりたい #バイクのある生活 #バイクのニュース #BikeHub \n {base_url}/{news.news_id}'
        api.update_status(status=message)

        news.is_posted = True
        news.save()
