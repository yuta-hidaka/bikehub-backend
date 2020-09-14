from django.http import Http404
from django.shortcuts import render


def complete(request):
    return render(request, 'account/account_confirm_complete.html')


def privacy(request):
    return render(request, 'account/privacy_policy.html')
