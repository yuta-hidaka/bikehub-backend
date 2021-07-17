from allauth.account.views import PasswordResetFromKeyView
from django.conf import settings
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


class SellerPasswordChangeView(PasswordResetFromKeyView):
    success_url = getattr(settings, "SELLER_BASE_URL", None) + '/seller'
