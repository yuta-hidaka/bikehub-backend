from django.test import TestCase

from .models import CustomUserManager


class UserTestCase(TestCase):
    def test_create_user(self):
        data = {
            'email': 'test@test.com',
            'password': 'test@test.com',
            'disp_name': 'hola'
        }

        res = CustomUserManager().create_user(
            email=data.pop('email'),
            password=data.pop('password'),
            extra_fields=data
        )

        print(res)
