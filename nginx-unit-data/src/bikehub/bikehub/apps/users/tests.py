from django.test import TestCase

from .models import BaseUserManager

# Create your tests here.


class SellerTestCase(TestCase):
    fixtures = ['plans.json', 'status.json', 'fc.json']

    def test_user_invite(self):
        a = BaseUserManager()
        a = a.invite_user(
            email="hoge"
        )
