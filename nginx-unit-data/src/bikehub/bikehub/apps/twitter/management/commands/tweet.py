import pathlib

import tweepy
from _facebook.service.post_facebook import post
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Q
from news.models import News


class Command(BaseCommand):
    def handle(self, **options):
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token = settings.TWITTER_ACCESS_TOKEN
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        base_url = 'https://web.bikehub.pw/article'
        base_url = 'https://web.bikehub.app/article'

        news = News.objects.\
            filter(~Q(featured_image=''), is_posted=False, show=True)\
            .order_by('-created_at').first()

        if not news:
            return

        img_url = news.featured_image
        extension = pathlib.Path(img_url).suffix

        if not extension:
            return

        author = news.source_site.name if news.site.is_there_another_source else news.site.name

        message = f'【BikeHubニュース便】\n - {author} - {news.title} \n #バイク好きと繋がりたい #バイクのある生活 #バイクのニュース #BikeHub\n'
        url = f'{base_url}/{news.news_id}'

        try:
            # Post to facebook
            post(message, url)

            diff = (len(message) + len(url)) - 140

            # trancate for tweet limit
            if diff > 0:
                title = news.title[:((len(news.title)) - (diff + 10))] + '...'
                message = f'【BikeHubニュース便】\n - {author} - {title} \n #バイク好きと繋がりたい #バイクのある生活 #バイクのニュース #BikeHub\n'

            api.update_status(status=f'{message}{url}')
        except Exception as e:
            send_mail(
                '【Tweet result】',
                f'you got error \n {e}',
                'batch@bikehub.app',
                ['yuta322@gmail.com'],
                fail_silently=False,
            )
        news.is_posted = True
        news.save()
