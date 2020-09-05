from django.shortcuts import render

# Create your views here.

from django.contrib.auth.views import PasswordResetView
from django.contrib import admin


class CustomResetPasswordView(PasswordResetView):
    def get_context_data(self, **kw):
        context = super().get_context_data(**kw)
        print("------------------------------------------------------------")
        print(context)
        print("------------------------------------------------------------")
        # context['site_name'] = getattr(admin.sites, 'site_name')  # get site header text. For django 2.X it should be getattr(admin.sites.AdminSite, 'site_header')
        return context
