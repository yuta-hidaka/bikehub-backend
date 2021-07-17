from django.urls import path

from .views import Portal, subscriptionCompanyCreate, subscriptionHooks

urlpatterns = [
    path('create', subscriptionCompanyCreate.as_view()),
    path('hooks', subscriptionHooks.as_view()),
    path('portal', Portal.as_view()),
]
