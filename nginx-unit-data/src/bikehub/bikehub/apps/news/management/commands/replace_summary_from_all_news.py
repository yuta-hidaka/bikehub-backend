from django.core.management.base import BaseCommand
from news.service.summary import Summary


class Command(BaseCommand):
    def handle(self, **options):
        Summary().create_summary_from_all_news()
