"""bikehub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

admin.site.site_header = 'Bike Hub'
admin.site.index_title = 'Bike Hub'
admin.site.site_title = 'Bike Hub'
admin.site.site_name = 'Bike Hub'
admin.autodiscover()

urlpatterns = [
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('rest/', include('rest.urls')),
    path('rest/auth/', include('dj_rest_auth.urls')),
    path('rest/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('web/admin/', admin.site.urls),
    path('web/accounts/', include('allauth.urls')),
    path('', include('users.urls')),
    path('sitemap', include('bikehub_web_app.urls')),

    path(
        'web/auth/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/custom_password_reset_form.html'
        ),
        name='admin_password_reset',
    ),
    path(
        'web/auth/reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/custom_password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/custom_password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/custom_password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
]
