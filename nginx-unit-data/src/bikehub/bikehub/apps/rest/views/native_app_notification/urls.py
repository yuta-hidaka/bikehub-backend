from django.contrib import admin
from django.urls import path, include
from .views import PushNotificationTokensList
urlpatterns = [
    # ---------------------------------------------------------
    path(
        'token/',
        PushNotificationTokensList.as_view(),
        name='token-list'
    ),
    # ---------------------------------------------------------
]
