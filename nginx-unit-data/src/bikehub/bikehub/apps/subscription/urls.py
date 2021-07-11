from django.urls import path

from .views import Portal, subscriptionCompanyCreate, subscriptionHooks

urlpatterns = [
    path('create', subscriptionCompanyCreate),
    path('hooks', subscriptionHooks),
    path('portal', Portal.as_view()),
]
