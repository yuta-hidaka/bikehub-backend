from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import PasswordResetView, SetPasswordForm
from django.contrib import admin


class CustomResetPasswordView(PasswordResetView):
    def get_context_data(self, **kw):
        context = super().get_context_data(**kw)
        return context


class CustomSetPasswordFormView(SetPasswordForm):
    def get_context_data(self, **kw):
        context = super().get_context_data(**kw)
        return context
