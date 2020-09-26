from django.http import Http404
from django.shortcuts import render


def index(request):
    return render(request, 'account/index.html')


def complete(request):
    return render(request, 'account/account_confirm_complete.html')


def privacy(request):
    return render(request, 'account/privacy_policy.html')


def support(request):
    return render(request, 'account/support.html')
