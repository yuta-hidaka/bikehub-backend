from django.core.management.base import BaseCommand
from native_app_notification.service.notifications import Notifications
from news.models import News
from django.conf import settings
from pytz import timezone
from native_app_notification.models import PushNotificationTokens, PushNotificationSettings
from concurrent.futures import ThreadPoolExecutor


class Command(BaseCommand):
    def handle(self, **options):
        self.notifications = Notifications()
        self.news = News.objects.order_by('-created_at').first()
        settings_time_zone = timezone(settings.TIME_ZONE)
        self.created_at = self.news.created_at.astimezone(settings_time_zone)
        self.setting = PushNotificationSettings.objects.get(pk=1)

        tokens = PushNotificationTokens.objects.all()
        with ThreadPoolExecutor() as w:
            w.map(self.push_notification, tokens)

    def push_notification(self, token):
        data = {
            'news_id': str(self.news.news_id),
            'title': self.news.title,
            'author': self.news.site.name,
            'imgUrl': self.news.featured_image,
            'summary': self.news.summary,
            'url': self.news.url,
            'created_at': str(self.created_at)
        }
        r = self.notifications.send_notification(
            token=token.token,
            target_url=self.setting.target_url,
            title=self.setting.title,
            body=f'{self.news.title}',
            data=data
        )

        print(r)
