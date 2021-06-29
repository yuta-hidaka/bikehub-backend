from django.contrib import admin
from django.urls import include, path

from .views import subscriptionCompanyCreate

urlpatterns = [
    path('company/subscription/create', subscriptionCompanyCreate),
]
