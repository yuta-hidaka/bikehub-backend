# Create your tests here.
import uuid

from django.core.management.base import BaseCommand
from subscription.tests import fake_subscription_create
from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, **_):

        email = f"foo+{uuid.uuid4()}@ex.xom"
        print("hi")

        user, company = fake_subscription_create()
        CustomUser.objects.invite_user_to_company(
            email=email,
            invited_by=user,
            company=company,
            first_name='',
            last_name=''
        )
