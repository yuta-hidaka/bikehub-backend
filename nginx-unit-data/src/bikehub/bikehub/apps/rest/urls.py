from django.urls import include, path

urlpatterns = [
    path('news/', include('rest.views.news.urls')),
    path('company/', include('rest.views.company.urls')),
    path('push_notification/', include('rest.views.native_app_notification.urls')),
    path('bike/', include('rest.views.fuel_consumption.urls')),
    path('seller/', include('rest.views.seller.urls')),
]
