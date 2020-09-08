from django.core.management.base import BaseCommand
from native_app_notification.service.notifications import Notifications
from news.models import News
from django.conf import settings
from pytz import timezone


class Command(BaseCommand):
    def handle(self, **options):
        notifications = Notifications()
        news = News.objects.order_by('-created_at').first()
        settings_time_zone = timezone(settings.TIME_ZONE)
        created_at = news.created_at.astimezone(settings_time_zone)

        data = {
            'news_id': str(news.news_id),
            'title': news.title,
            'author': news.site.name,
            'imgUrl': news.featured_image,
            'summary': news.summary,
            'url': news.url,
            'created_at': str(created_at)
        }

        notifications.send_notification(
            token='ExponentPushToken[B9opxUHaIB7atnKGr_Te2c]',
            title='新しいニュースが届きました！',
            body=f'{news.title}',
            data=data
        )
