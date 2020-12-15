from datetime import datetime, timedelta
from time import sleep

import tweepy
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from twitter.models import FollowInfo


class Command(BaseCommand):
    def handle(self, **options):
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token = settings.TWITTER_ACCESS_TOKEN
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        seven_dayas_before = datetime.today() - timedelta(days=7)

        followers = [follower for follower in tweepy.Cursor(api.followers_ids).items()]

        non_followers = FollowInfo.objects.filter(
            is_followed=False, updated_at__lte=seven_dayas_before
        ).all()

        if not non_followers:
            return

        unfollow_cnt = 0
        for non_follower in non_followers:
            if non_follower not in followers:
                try:
                    api.destroy_friendship(non_follower.twitter_user_id)
                    non_follower.delete()
                    unfollow_cnt += 1
                    sleep(1)
                except Exception as e:
                    print(
                        f'you got error \n {e} \n non_follower.twitter_user_id: {non_follower.twitter_user_id}'
                    )
                    send_mail(
                        '【Unfollow result】',
                        f'you got error \n {e} \n non_follower.twitter_user_id: {non_follower.twitter_user_id}',
                        'batch@bikehub.app',
                        ['yuta322@gmail.com'],
                        fail_silently=False,
                    )
                    return
            else:
                non_follower.is_followed = True
                non_follower.save()

        send_mail(
            '【Unfollow result】',
            f'you unfollowed \n {unfollow_cnt} users',
            'batch@bikehub.app',
            ['yuta322@gmail.com'],
            fail_silently=False,
        )
