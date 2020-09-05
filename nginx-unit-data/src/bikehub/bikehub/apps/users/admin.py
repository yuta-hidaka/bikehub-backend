from django.utils.translation import ugettext_lazy
from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'disp_name',
        'email',
        'accept',
        'created_at'
    ]
    search_fields = [
        'email',
        'disp_name',
    ]


# Register your models here.
admin.site.register(
    CustomUser, CustomUserAdmin
)


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('My site admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('My administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Site administration')


admin_site = MyAdminSite()
