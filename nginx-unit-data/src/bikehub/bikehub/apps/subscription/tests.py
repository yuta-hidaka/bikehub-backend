from django.test import TestCase
from rest_framework.test import APIRequestFactory


class SubscriptionTestCase(TestCase):
    def test_animals_can_speak(self):
        factory = APIRequestFactory()
        data = {
            'first_name': 'first',
            'last_name': 'last',
            'email': 'test@test.com',
            'disp_name': 'TestSeller',
            'seller': True,
            'password': 'P@SSword9876',
            'password2': 'P@SSword9876',
            'gender': 0,
            'accept': True
        }
        factory.post('/rest/auth/registration', data)

    # def test_create_company_subscription(self):
    #     factory = APIRequestFactory()
    #     data = {
    #         'name': 'name',
    #         'post_code': 'post code',
    #         'city': 'city',
    #         'street': 'street',
    #         'building': 'building',
    #         'phone': '090888999',
    #         'email': 'hoge@hoge.com',
    #         'prefecture': 'aaaaa',
    #         'plan': 'pro'
            
    #     }
    #     res = factory.post('/subscription/create', data)

    #     print(res)

