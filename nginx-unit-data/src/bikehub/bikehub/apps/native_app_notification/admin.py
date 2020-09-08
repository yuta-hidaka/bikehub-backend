from django.contrib import admin
from .models import *


class PushNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'target_url',
        'title',
        'created_at'
    ]
    search_fields = [
        'target_url',
        'title',
        'id',
    ]


class PushNotificationTokensAdmin(admin.ModelAdmin):
    list_display = [
        'push_notification_tokens_id',
        'token',
        'is_active',
        'created_at'
    ]
    search_fields = [
        'push_notification_tokens_id',
        'token',
        'is_active',
    ]


# Register your models here.
admin.site.register(
    PushNotificationSettings, PushNotificationSettingsAdmin
)

# Register your models here.
admin.site.register(
    PushNotificationTokens, PushNotificationTokensAdmin
)
