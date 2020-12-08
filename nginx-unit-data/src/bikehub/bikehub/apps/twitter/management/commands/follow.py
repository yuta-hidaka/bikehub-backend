import time
from datetime import date

import tweepy
from django.conf import settings
from django.core.management.base import BaseCommand
from twitter.models import FollowInfo, SearchKeyWord

MAX_FOLLOW = 400


class Command(BaseCommand):
    def handle(self, **options):
        # If followe prccess is running retun
        proccessing_count = SearchKeyWord.objects.filter(is_proccessing=True).count()
        todays_followed_count = FollowInfo.objects.filter(created_at__date=date.today()).count()
        if proccessing_count != 0:
            return

        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        me = api.me()

        followers = [follower for follower in tweepy.Cursor(api.followers_ids).items()]
        friends = [friend for friend in tweepy.Cursor(api.friends_ids).items()]

        for friend in friends:
            if friend not in followers:
                FollowInfo.objects.get_or_create(twitter_user_id=friend)

        key_words = SearchKeyWord.objects.all()
        follow_count = todays_followed_count
        for key_word in key_words:
            key_word.is_proccessing = True
            key_word.save()

            tweets = api.search(q=key_word.key_word)
            for tweet in tweets:
                author = tweet.author
                if author.id not in followers and me.id != author.id:
                    try:
                        obj, created = FollowInfo.objects.get_or_create(twitter_user_id=author.id)
                        if created:
                            api.create_friendship(id=author.id)

                        follow_count += 1
                        if follow_count > MAX_FOLLOW:
                            key_word.is_proccessing = False
                            key_word.save()
                            return
                        time.sleep(5)
                    except Exception as e:
                        print(e)
                        key_word.is_proccessing = False
                        key_word.save()
                        return

            key_word.is_proccessing = False
            key_word.save()

    def add_followed_user(self, friends):
        pass
