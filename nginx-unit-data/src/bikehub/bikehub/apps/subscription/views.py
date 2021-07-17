import datetime
import json
from datetime import datetime, timedelta

import stripe
from company.models import Company, CompanyUserGroup
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser

from subscription.models import Plans, Status, Subscriptions

from .enum import StatusEnum

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)
SELLER_BASE_URL = getattr(settings, "SELLER_BASE_URL", None)


class Portal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *_, **__):
        company = Company.objects.get(
            admin=request.user,
            is_child=False,
        )

        subscription = Subscriptions.objects.get(
            company=company
        )

        session = stripe.billing_portal.Session.create(
            customer=subscription.stripe_customer_id,
            return_url=f"{SELLER_BASE_URL}/seller/registration/success",
        )

        return JsonResponse({'url': session.url})


class subscriptionHooks(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *_, **__):
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
        webhook_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)
        param = json.loads(request.body)
        if webhook_secret:
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
            except Exception as e:
                return e
            hook_type = event['type']
        else:
            hook_type = param['type']

        # print(json.dumps(param, indent=4, sort_keys=True))

        hook_type = param['type']

        def _toTime(time):
            return datetime.fromtimestamp(time)
        customer_id = param['data']['object'].get('customer')

        if customer_id is None:
            return HttpResponse(status=200)

        subscription = Subscriptions.objects.get(stripe_customer_id=customer_id)
        status = None
        if hook_type == 'customer.subscription.updated':
            if param['data']['object']['canceled_at'] is None:
                plan = Plans.objects.get(stripe_price_id=param['data']['object']['plan']['id'])
                # if subscription.plan != plan:
                #     # Recalculate capacity
                #     print('plan changed')
                status = Status.objects.get(code=StatusEnum.subscribing.value)
                subscription.expire = _toTime(param['data']['object']['current_period_end']) + timedelta(days=7)
                subscription.plan = plan
            else:
                status = Status.objects.get(code=StatusEnum.canceled.value)
            subscription.status = status
        elif hook_type == 'invoice.payment_succeeded':
            status = Status.objects.get(code=StatusEnum.subscribing.value)
        elif hook_type == 'payment_intent.payment_failed':
            status = Status.objects.get(code=StatusEnum.payment_failed.value)
        elif hook_type == 'customer.updated':
            subscription.company.email = param['data']['object']['email']
        elif hook_type == 'customer.subscription.deleted':
            status = Status.objects.get(code=StatusEnum.canceled.value)
        elif hook_type == 'invoice.payment_failed':
            status = Status.objects.get(code=StatusEnum.payment_failed.value)

        if status:
            subscription.status = status

        subscription.save()

        return HttpResponse(status=200)


class subscriptionCompanyCreate(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *_, **__):
        if request.method != "POST":
            raise PermissionDenied()

        param = json.loads(request.body)

        user = CustomUser.objects.get(
            email=param['user']['email']
        )

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

        aa = CompanyUserGroup.objects.create(
            company=company,
            user=user,
            permission=CompanyUserGroup.Permissions.ADMIN
        )

        print(aa.permission)

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
            success_url=f"{SELLER_BASE_URL}/seller/registration/success",
            cancel_url=f"{SELLER_BASE_URL}/seller/registration/cancel",
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
