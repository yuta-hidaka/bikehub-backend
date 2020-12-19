import json
import re
from concurrent.futures import ThreadPoolExecutor
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.core.management.base import BaseCommand
from native_app_notification.models import (PushNotificationSettings,
                                            PushNotificationTokens)
from native_app_notification.service.notifications import Notifications
from news.models import News
from pytz import timezone


class Command(BaseCommand):
    def handle(self, **options):
        self.notifications = Notifications()
        self.news = News.objects.order_by('-created_at').first()
        settings_time_zone = timezone(settings.TIME_ZONE)
        self.created_at = self.news.created_at.astimezone(settings_time_zone)
        self.setting = PushNotificationSettings.objects.get(pk=1)
        slice_limit = self.setting.push_notification_send_unit
        limit = slice_limit
        offset = 0

        token_count = PushNotificationTokens.objects.values('token').count()
        token_loop_count = \
            int(
                Decimal(str(token_count / slice_limit))
                .quantize(Decimal('0'), rounding=ROUND_HALF_UP)
            )

        for i in range(token_loop_count):

            token_list = PushNotificationTokens\
                .objects.values('token')[offset:limit]

            tokens = [
                i.get('token', '') for i in token_list if i.get('token', '')
            ]

            self.push_notification(tokens)
            offset += slice_limit
            limit += slice_limit

    def push_notification(self, tokens):
        r = self.notifications.send_notification(
            tokens=tokens,
            target_url=self.setting.target_url,
            title="アプリの不具合のご連絡",
            body="一時期アプリがクラッシュする事象が発見されました。現在修正されましたので、アプリを数回再起動することで修正されます。",
            data={}
        )

        token_status_list = json.loads(r.text).get('data', None)

        if token_status_list:
            with ThreadPoolExecutor(max_workers=10) as e:
                e.map(self.token_validator, token_status_list)

    def token_validator(self, token_status):
        status = token_status.get('status', None)
        detail = token_status.get('details', None).get('error', None)
        if status == 'error' and detail == 'DeviceNotRegistered':
            message = token_status.get('message', None)
            try:
                invalid_token = re.search('"(.+?)"', message).group(1)
                PushNotificationTokens.objects \
                    .filter(token=invalid_token).delete()
            except Exception as e:
                print(e)
