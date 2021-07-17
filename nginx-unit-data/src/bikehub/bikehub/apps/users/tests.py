from django.test import TestCase
from subscription.tests import fake_subscription_create

from .models import CustomUser

# Create your tests here.


class SellerTestCase(TestCase):
    fixtures = ['plans.json', 'status.json', 'fc.json']

    def test_inviteuser_company(self):

        email = 'test@ex.com'

        user, company = fake_subscription_create()
        CustomUser.objects.invite_user_to_company(
            email=email,
            invited_by=user,
            company=company,
            first_name='',
            last_name=''
        )
