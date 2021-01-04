import time
from datetime import datetime, timedelta

import tweepy
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from twitter.models import FollowInfo, SearchKeyWord


class TwitterAutomation():
    def __init__(self):
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token = settings.TWITTER_ACCESS_TOKEN
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
