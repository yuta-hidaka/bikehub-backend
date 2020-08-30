from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('news/', include('rest.views.news.urls')),
    path('bike/', include('rest.views.fuel_consumption.urls')),
]
