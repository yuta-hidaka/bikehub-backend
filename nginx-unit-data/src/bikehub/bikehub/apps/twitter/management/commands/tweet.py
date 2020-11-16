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

        news = News.objects.\
            filter(~Q(featured_image=''), is_posted=False)\
            .order_by('-created_at').first()

        img_url = news.featured_image
        extension = pathlib.Path(img_url).suffix

        if not extension:
            return

        filename = f'tnp.{extension}'
        message = f'【BikeHubニュース便】 \n {news.title} \nニュースはこちら→ {news.url} \n #バイク好きと繋がりたい #バイクのある生活'
        request = requests.get(img_url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            try:
                api.update_with_media(filename=filename, status=message)
            except Exception as e:
                print(e)
                pass

            os.remove(filename)
        else:
            print("Unable to download image")
