import time

import tweepy
from django.conf import settings
from django.core.management.base import BaseCommand
from twitter.models import FollowInfo, SearchKeyWord

MAX_FOLLOW = 490


class Command(BaseCommand):
    def handle(self, **options):
        # If followe prccess is running retun
        proccessing_count = SearchKeyWord.objects.filter(is_proccessing=True).count()
        if proccessing_count != 0:
            return

        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        followers = [follower for follower in tweepy.Cursor(api.followers_ids).items()]
        key_words = SearchKeyWord.objects.all()
        follow_count = 1
        for key_word in key_words:
            key_word.is_proccessing = True
            key_word.save()

            for _ in range(50):
                since_id = 0
                tweets = api.search(q=key_word.key_word, since_id=since_id)
                since_id = tweets.since_id

                for tweet in tweets:
                    author = tweet.author
                    if author.id not in followers:
                        try:
                            api.create_friendship(id=author.id)
                            FollowInfo.objects.get_or_create(twitter_user_id=author.id)
                            follow_count += 1
                            if follow_count > MAX_FOLLOW:
                                return
                            time.sleep(5)
                        except Exception as e:
                            print(e)
                            key_word.is_proccessing = False
                            key_word.save()
                            return

            key_word.is_proccessing = False
            key_word.save()
