from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('news/', include('rest.views.news.urls')),
    path('company/', include('rest.views.company.urls')),
    path('push_notification/', include('rest.views.native_app_notification.urls')),
    path('bike/', include('rest.views.fuel_consumption.urls')),
]
