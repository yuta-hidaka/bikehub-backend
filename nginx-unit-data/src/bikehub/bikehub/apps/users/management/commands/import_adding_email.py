import json

from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, **options):
        print("adding Email")
        users = CustomUser.objects.all()

        for user in users:
            EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                verified=True,
                primary=True
            )
