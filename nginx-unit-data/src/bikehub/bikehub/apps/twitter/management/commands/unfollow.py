import json
import os
import pathlib

import requests
import tweepy
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from time import sleep


class Command(BaseCommand):
    def handle(self, **options):
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        friends = [friend for friend in tweepy.Cursor(api.friends_ids).items()]
        followers = [follower for follower in tweepy.Cursor(api.followers_ids).items()]
        not_followers = [friend for friend in friends if friend not in followers]

        for not_follower in not_followers:
            api.destroy_friendship(not_follower)
            sleep(0.5)

        # friend = api.show_friendship(target_id=1049624023007555584)

        # # print(friend[0])

        # a = api.followers()

        # for i in a:
        #     print(json.dumps(i._json, ensure_ascii=False))
