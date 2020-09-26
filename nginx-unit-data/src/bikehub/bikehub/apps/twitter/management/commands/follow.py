from django.core.management.base import BaseCommand
from django.conf import settings
import tweepy
import time


class Command(BaseCommand):
    def handle(self, **options):
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #     print(tweet.text)

        # user = api.search('バイク')
        me = api.me()
        print(me.followers_count)

        for follower in self.limit_handled(tweepy.Cursor(api.followers).items()):
            if follower.friends_count < 300:
                print(follower.screen_name)

        # for friend in user:
        #     print(friend.user.screen_name)

    def limit_handled(self, cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                print("error")
                # time.sleep(15 * 60)
