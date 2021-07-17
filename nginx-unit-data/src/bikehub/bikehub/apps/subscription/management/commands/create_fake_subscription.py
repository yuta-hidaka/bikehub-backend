from django.core.management.base import BaseCommand
from subscription.tests import fake_subscription_create


class Command(BaseCommand):
    def handle(self, **_):
        fake_subscription_create()
