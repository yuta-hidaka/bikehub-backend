from django.core.management.base import BaseCommand
from news.models import *
from ...service.collect_news import CollectNews


class Command(BaseCommand):
    def handle(self, **options):
        CollectNews().collect_news()
