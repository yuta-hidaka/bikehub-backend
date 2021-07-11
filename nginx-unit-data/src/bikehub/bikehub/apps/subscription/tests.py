import json
import subprocess
import uuid

from django.contrib.auth.hashers import check_password
from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser


class SubscriptionTestCase(TestCase):
    fixtures = ['plans.json', 'status.json']

    def test_subscription_create(self):
        client = APIClient()
        email = f'test+{uuid.uuid4()}@test.com'
        data = {
            'first_name': 'first',
            'last_name': 'last',
            'email': email,
            'disp_name': 'TestSeller',
            'seller': True,
            'password': 'P@SSword9876',
            'password2': 'P@SSword9876',
            'gender': 0,
            'accept': True
        }
        res = client.post('/rest/auth/registration/', data, format='json')

        user = CustomUser.objects.get(email=data['email'])

        assert user.first_name == data['first_name']
        assert user.last_name == data['last_name']
        assert user.email == data['email']
        assert user.disp_name == data['disp_name']
        assert user.seller == data['seller']
        assert user.gender == data['gender']
        assert user.accept == data['accept']
        assert check_password(data['password'], user.password)

        subscription_data = {
            'user': data,
            'company': {
                'name': 'name',
                'post_code': 'post code',
                'city': 'city',
                'street': 'street',
                'building': 'building',
                'phone': '090888999',
                'email': email,
                'prefecture': 'aaaaa',
            },
            'plan': 'pro'
        }
        res = client.post('/subscription/create', subscription_data, format='json')

        print(res.json()['checkout_url'])
        assert res.json()['checkout_url'] != ''
        client.login(username=data['email'], password=data['password'])
        res = client.post('/subscription/portal', subscription_data, format='json')

        print('')
        print(res.json()['url'])
        assert res.json()['url'] != ''
