from django.contrib import admin
from django.urls import include, path

from .views import customerPortal, subscriptionCompanyCreate, subscriptionHooks

urlpatterns = [
    path('company/subscription/create', subscriptionCompanyCreate),
    path('company/subscription/hooks', subscriptionHooks),
    path('company/subscription/portal', customerPortal),
]
