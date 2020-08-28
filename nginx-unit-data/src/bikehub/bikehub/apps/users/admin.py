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
    CustomUser,CustomUserAdmin
)