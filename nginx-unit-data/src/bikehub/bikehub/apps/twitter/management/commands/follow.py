import time
from datetime import datetime, timedelta
from typing import List

import tweepy
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from twitter.models import FollowInfo, SearchKeyWord

MAX_FOLLOW = 100


class Command(BaseCommand):
    def __init__(self):
        self.follow_count = 0

    def handle(self, **options):
        date_from = datetime.now() - timedelta(days=1)
        # If followe prccess is running retun
        todays_followed_count = FollowInfo.objects.filter(created_at__gte=date_from).count()

        if todays_followed_count >= MAX_FOLLOW:
            send_mail(
                '【follow result】',
                f'limmit reached \n todays_followed_count :{todays_followed_count}',
                'batch@bikehub.app',
                ['yuta322@gmail.com'],
                fail_silently=False,
            )
            return

        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token = settings.TWITTER_ACCESS_TOKEN
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

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
        self.follow_count = todays_followed_count
        for key_word in key_words:

            # 1035162720260128770
            users = api.search_users(q=key_word.key_word, count=20)
            for user in users:
                count, is_stop = self.follow_user(followers, me, user.id, api, key_word)
                if is_stop:
                    self.send_follow_result()
                    return

            tweets = api.search(q=key_word.key_word)

            def __follow_by_tweet(tweets):
                tweet_count = 5
                for tweet in tweets:
                    if tweet_count == 0:
                        return
                    self.follow_user(followers, me, tweet.author.id, api, key_word)
                    if is_stop:
                        return is_stop
                    tweet_count -= 1
                return False

            __follow_by_tweet(tweets)
            if is_stop:
                self.send_follow_result()
                return

    def add_followed_user(self, friends):
        pass

    def follow_by_search_user(self) -> List[int]:
        pass

    def follow_user(self, followers, me, user_id, api, key_word) -> List[int]:
        is_stop = False

        if self.follow_count > MAX_FOLLOW:
            self.send_follow_result()
            is_stop = True
            return self.follow_count

        if user_id in followers or me.id == user_id:
            return self.follow_count, is_stop

        try:
            obj, created = FollowInfo.objects.get_or_create(twitter_user_id=user_id)
            if not created:
                return self.follow_count, is_stop

            api.create_friendship(id=user_id)
            time.sleep(15)
            self.follow_count += 1

        except Exception as e:
            if e.api_code == 162:
                pass
            else:
                self.send_error_message(e)

        return self.follow_count, is_stop

    def follow_by_search_tweet(self) -> List[int]:
        pass

    def send_follow_result(self):
        send_mail(
            '【follow result】',
            f'you followed \n {self.follow_count} users',
            'batch@bikehub.app',
            ['yuta322@gmail.com'],
            fail_silently=False,
        )

    @staticmethod
    def send_error_message(error: Exception):
        send_mail(
            '【follow result】',
            f'you got error \n {error}',
            'batch@bikehub.app',
            ['yuta322@gmail.com'],
            fail_silently=False,
        )
