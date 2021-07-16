import uuid

from django.core.management.base import BaseCommand
from django.test import TestCase
from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, **_):
        email = f"foo+{uuid.uuid4()}@ex.xom"
        CustomUser.objects.invite_user(
            email=email, 
            first_name='',
            last_name=''
        )
