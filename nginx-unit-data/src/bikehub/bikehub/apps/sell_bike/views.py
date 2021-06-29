import json

import stripe
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser

from .models import Company

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)
DEBUG = getattr(settings, "DEBUG", None)
PLANS = {
    'business': 'price_1J7iYzJ3tmwMMj97vE7taAZT',
    'pro': 'price_1J7iZXJ3tmwMMj97ZVunFUgJ',
    'starter': 'price_1J7ia6J3tmwMMj97MZpcp7V4',
}

BASE_URL = 'https://web.bikehub.pw' if not DEBUG else 'http://localhost:3000'


@csrf_exempt
def subscriptionCompanyCreate(request):
    if request.method != "POST":
        raise PermissionDenied()

    param = json.loads(request.body)

    user = CustomUser.objects.filter(
        email=param['user']['email']
    ).first()

    if(DEBUG and user is None):
        user = CustomUser.objects.filter(
            username='yuta322@gmail.com'
        ).first()
    company = Company.objects.create(
        plan=param['plan'],
        name=param['company']['name'],
        stripe_customer_id="",
        admin=user,
        address=param['company']['address'],
        email=param['company']['email'],
        phone=param['company']['phone'],
        post_code=param['company']['post_code'],
        prefecture=param['company']['prefecture']
    )

    res = stripe.Customer.create(
        description=f"{param['company']['name']}",
        email=param['company']['email'],
    )

    company.stripe_customer_id = res['id']
    company.save()

    res = stripe.checkout.Session.create(
        success_url=f"{BASE_URL}/seller/registration/success",
        cancel_url=f"{BASE_URL}/seller/registration/cancel",
        payment_method_types=["card"],
        line_items=[
            {
                'price': PLANS[param['plan']],
                'quantity': 1,
            },
        ],
        mode="subscription",
        customer=res['id']
    )

    return JsonResponse({'checkout_url': res['url']})
