import pathlib

import tweepy
from _facebook.service.post_facebook import post
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Q
from news.models import News

TAG_DISALLOW_LIST = ['事故', '死亡', '殺人', '盗']


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
        # base_url = 'https://web.bikehub.app/article'

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

        def _avoid_tag():
            for t in TAG_DISALLOW_LIST:
                if t in news.title + news.summary:
                    return True

                return False

        tags = ''
        tweet_title = 'BikeHub | ニュース便'

        if _avoid_tag():
            tags = '#ニュース #バイクのニュース #BikeHub'
        elif news.is_youtube:
            tags = '#バイク好きと繋がりたい #モトブロガーさんご紹介 #モトブログ #BikeHub'
            tweet_title = 'BikeHub | モトブロガーさんご紹介'
        else:
            tags = '#バイク好きと繋がりたい #バイクのある生活 #バイクのニュース #BikeHub'

        message = f'【{tweet_title}】\n - {author} - {news.title} \n {tags}\n'
        url = f'{base_url}/{news.news_id}'

        try:
            # Post to facebook
            post(message, url)

            diff = (len(message) + len(url)) - 140

            # trancate for tweet limit
            if diff > 0:
                title = news.title[:((len(news.title)) - (diff + 10))] + '...'
                message = f'【{tweet_title}】\n - {author} - {title} \n {tags}\n'

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
