from django.urls import path

from .views import P, Portal, subscriptionCompanyCreate, subscriptionHooks

urlpatterns = [
    path('create', subscriptionCompanyCreate),
    path('hooks', subscriptionHooks),
    path('portal', Portal.as_view()),
    path('p', P.as_view()),
]
