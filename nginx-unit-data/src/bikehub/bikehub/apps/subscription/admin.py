from django.contrib import admin

from .models import Plans, Subscriptions


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'company',
        'plan',
        'status',
        'created_at',
    ]
    search_fields = [
        'company',
        'created_at',
        'plan',
        'status',
    ]
    ordering = ['-created_at']


admin.site.register(Subscriptions, SubscriptionAdmin)
admin.site.register(Plans)
