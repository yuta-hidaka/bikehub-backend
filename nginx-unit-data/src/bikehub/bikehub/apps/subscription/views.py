import datetime
import json

import stripe
from company.models import Company, CompanyUserGroup
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.models import CustomUser

from subscription.models import Plans, Status, Subscriptions

from .enum import StatusEnum

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)
DEBUG = getattr(settings, "DEBUG", None)


BASE_URL = 'https://web.bikehub.pw' if not DEBUG else 'http://localhost:3000'


class P(APIView):
    def post(self, request, *args, **kwargs):
        print("hi")
        pass

    def get(self, request, *args, **kwargs):
        print("hi")
        pass


class Portal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(
            admin=request.user,
            is_child=False,
        )

        subscription = Subscriptions.objects.get(
            company=company
        )

        session = stripe.billing_portal.Session.create(
            customer=subscription.stripe_customer_id,
            return_url=f"{BASE_URL}/seller/registration/success",
        )

        return JsonResponse({'url': session.url})


@csrf_exempt
def subscriptionHooks(request):
    """
        PS C:\stripe_cli> ./stripe.exe  listen --forward-to localhost/company/subscription/hooks
        > Ready! Your webhook signing secret is whsec_yxhRYnZMtKmoiulfM6og8kjv4DB4zFuz
        PS C:\stripe_cli> ./stripe.exe  listen --forward-to localhost:8000/company/subscription/hooks
        > Ready! Your webhook signing secret is whsec_yxhRYnZMtKmoiulfM6og8kjv4DB4zFuz (^C to quit)
        charge.succeeded
        charge.refunded

{
    "api_version": "2020-08-27",
    "created": 1625494305,
    "data": {
        "object": {
            "address": null,
            "balance": 0,
            "created": 1625494305,
            "currency": null,
            "default_source": null,
            "delinquent": false,
            "description": "\u500b\u4eba\u4e8b\u696d\u4e3b",
            "discount": null,
            "email": "yuta322+898999@gmail.com",
            "id": "cus_JnTTJ0OtAkmW7i",
            "invoice_prefix": "A47B3FFA",
            "invoice_settings": {
                "custom_fields": null,
                "default_payment_method": null,
                "footer": null
            },
            "livemode": false,
            "metadata": {},
            "name": null,
            "next_invoice_sequence": 1,
            "object": "customer",
            "phone": null,
            "preferred_locales": [],
            "shipping": null,
            "tax_exempt": "none"
        }
    },
    "id": "evt_1J9sWTJ3tmwMMj97T1J1CNkW",
    "livemode": false,
    "object": "event",
    "pending_webhooks": 1,
    "request": {
        "id": "req_crFu9wlTUIcYJD",
        "idempotency_key": "dde830cb-83d6-4dd1-ae53-2c25701f14bf"
    },
    "type": "customer.created"
}




    """
    param = json.loads(request.body)
    print(json.dumps(param, indent=4, sort_keys=True))

    hook_type = param['type']

    """
        ・プラン変更時
            ・プラン変更時すぐに上限解放
        ・決済完了時(次回期限日はperiod_end+21日(3weeks))
            ・決済完了ごとに上限をリセットする。
        ・サブスクキャンセル時
            ・キャンセルしても期限日+21日(3weeks))まで使用できる
        ・サブスク再開時
            ・未考慮
    """

    if hook_type == 'customer.subscription.updated':
        subscription = Subscriptions.objects.get(
            stripe_customer_id=param['data']['object']['plan']['customer']
        )
        if param['data']['object']['canceled_at'] != 'null':
            status = Status.objects.get(code=StatusEnum.canceled.value)
        else:
            plan = Plans.objects.get(stripe_price_id=['data']['object']['plan']['id'])
            status = Status.objects.get(code=StatusEnum.subscribing.value)
            subscription.plan = plan
        subscription.status = status
        subscription.save()
    elif hook_type == 'invoice.payment_succeeded':
        subscription = Subscriptions.objects.get(
            stripe_customer_id=param['data']['object']['plan']['customer']
        )
        status = Status.objects.get(code=StatusEnum.subscribing.value)
        subscription.status = status
        period_start = param['data']['object']['period_start']
        period_end = param['data']['object']['period_end']
    elif hook_type == 'payment_intent.payment_failed':
        subscription = Subscriptions.objects.get(
            stripe_customer_id=param['data']['object']['plan']['customer']
        )
        status = Status.objects.get(code=StatusEnum.payment_failed.value)
        subscription.status = status
        subscription.save()
    elif hook_type == 'customer.updated':
        subscription = Subscriptions.objects.get(
            stripe_customer_id=param['data']['object']['id']
        )
        subscription.company.email = param['data']['object']['email']
        subscription.save()

    return HttpResponse(status=200)


@csrf_exempt
def subscriptionCompanyCreate(request):
    if request.method != "POST":
        raise PermissionDenied()

    param = json.loads(request.body)

    user = CustomUser.objects.get(
        email=param['user']['email']
    )

    if(DEBUG and user is None):
        user = CustomUser.objects.filter(
            username='yuta322@gmail.com'
        ).first()

    exists = Company.objects.filter(
        email=param['company']['email'],
    ).exists()
    # NOTE When proccess killed this user already registered so they can not re-registare .
    if(exists):
        return JsonResponse(
            status=400,
            data={
                'status': 'false',
                'message': 'すでにこのメールアドレスは登録されています。ログインしてプラン変更のお申し込みを行ってください。'
            }
        )

    res = stripe.Customer.create(
        description=f"{param['company']['name']}",
        email=param['company']['email'],
    )

    company = Company.objects.create(
        name=param['company']['name'],
        admin=user,
        street=param['company']['street'],
        city=param['company']['city'],
        building=param['company']['building'],
        email=param['company']['email'],
        phone=param['company']['phone'],
        post_code=param['company']['post_code'],
        prefecture=param['company']['prefecture']
    )

    CompanyUserGroup.objects.create(
        company=company,
        user=user,
        permission='admin'
    )

    plan = Plans.objects.get(
        name=param['plan']
    )

    status = Status.objects.get(code=StatusEnum.payment_waiting.value)

    Subscriptions.objects.create(
        company=company,
        plan=plan,
        status=status,
        stripe_customer_id=res['id']
    )

    res = stripe.checkout.Session.create(
        success_url=f"{BASE_URL}/seller/registration/success",
        cancel_url=f"{BASE_URL}/seller/registration/cancel",
        payment_method_types=["card"],
        line_items=[
            {
                'price': plan.stripe_price_id,
                'quantity': 1,
            },
        ],
        mode="subscription",
        customer=res['id']
    )

    return JsonResponse({'checkout_url': res['url']})
