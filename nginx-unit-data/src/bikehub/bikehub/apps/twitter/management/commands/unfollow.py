from datetime import datetime, timedelta
from time import sleep

import tweepy
from django.conf import settings
from django.core.management.base import BaseCommand
from twitter.models import FollowInfo


class Command(BaseCommand):
    def handle(self, **options):
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        seven_dayas_before = datetime.today() + timedelta(days=7)

        followers = [follower for follower in tweepy.Cursor(api.followers_ids).items()]

        non_followers = FollowInfo.objects.filter(
            is_followed=False, updated_at__lte=seven_dayas_before
        ).all()

        if not non_followers:
            return

        for non_follower in non_followers:
            if non_follower not in followers:
                api.destroy_friendship(non_follower.twitter_user_id)
                non_follower.delete()
                sleep(1)
            else:
                non_follower.is_followed = True
                non_follower.save()
