# Create your tests here.
import uuid

from company.models import CompanyUserGroup
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Permission
from django.test import TestCase
from fuel_consumption.models import Bike
from rest_framework import permissions
from rest_framework.test import APIClient
from subscription.tests import fake_subscription_create, fake_user_create
from users.models import CustomUser


class SellerTestCase(TestCase):
    fixtures = ['plans.json', 'status.json', 'fc.json']

    def test_product_create(self):
        client = APIClient()
        user, company = fake_subscription_create()
        user2, data = fake_user_create()
        user3, _ = fake_user_create()
        user4, _ = fake_subscription_create()
        bike = Bike.objects.all().first()
        CompanyUserGroup.objects.create(
            user=user2,
            company=company,
            permission=CompanyUserGroup.Permissions.EDITOR
        )
        CompanyUserGroup.objects.create(
            user=user3,
            company=company,
            permission=CompanyUserGroup.Permissions.VIEWER
        )

        client.force_authenticate(user=user)

        data = {
            'product': 'MOTO',
            'color': '#2DC200',
            'company': company.pk,
            'moto': bike.pk,
            'title': 'test product',
            'description': 'aaaaaaaaaaaa',
            'price': 9999,
            'total_price': 99999,
            'model_year': 2013,
            'vehicle_inspection': '2022-01-22',
            'mileage': 9999,
            'displacement': 999,
            'electric_power': 222,
            'custom': True,
            'abs': True,
            'sel_on_web': True,
            'led': True,
            'maker_warranty': True,
            'seller_warranty': True,
            'etc': True,
            'navigation': True,
            'fi': True,
            'four_storoke': True,
            'mt': True,
            'reimport': True,
            'repaired': True,
            'free_oil_change': True,
            'free_maintenance': True,
            'security': True,
            'electric_bike': True,
            'images': [],
            'comments': [],
        }

        res = client.post('/rest/seller/products/', data, format='json')
        result = res.json()

        for k, v in data.items():
            if type(v) is bool:
                assert v is result[k]
            elif type(v) is uuid.UUID:
                assert v == uuid.UUID(result[k])
            else:
                assert v == result[k]

        assert user.pk == uuid.UUID(result['created_by'])

        client.force_authenticate(user=None)
        client.force_authenticate(user=user2)
        data['title'] = 'editooooo'
        res = client.put(f'/rest/seller/product/{result["product_id"]}/', data, format='json')
        result = res.json()

        for k, v in data.items():
            if type(v) is bool:
                assert v is result[k]
            elif type(v) is uuid.UUID:
                assert v == uuid.UUID(result[k])
            else:
                assert v == result[k]

        assert user2.pk == uuid.UUID(result['updated_by'])
        assert user.pk == uuid.UUID(result['created_by'])

        client.force_authenticate(user=user3)
        res = client.put(f'/rest/seller/product/{result["product_id"]}/', data, format='json')

        assert res.status_code == 403

        client.force_authenticate(user=user4)
        data['title'] = 'editooooo unauthorized'
        res = client.put(f'/rest/seller/product/{result["product_id"]}/', data, format='json')

        assert res.status_code == 403
