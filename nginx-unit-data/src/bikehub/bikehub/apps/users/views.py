from django.conf import settings
from django.contrib.auth import views as auth_views
from django.shortcuts import render


def index(request):
    # return redirect('https://www.bikehub.app/')
    # return render(request, 'out_publish/index.html')
    return render(request, 'account/index.html')


def complete(request):
    return render(request, 'account/account_confirm_complete.html')


def privacy(request):
    return render(request, 'account/privacy_policy.html')


def support(request):
    return render(request, 'account/support.html')


class SellerPasswordChangeView(auth_views.PasswordResetView):
    SELLER_BASE_URL = getattr(settings, "SELLER_BASE_URL", None)
    success_url = "SELLER_BASE_URL"
    pass
