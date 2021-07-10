from django.contrib import admin

from .models import Plans, Subscriptions

admin.site.register(Subscriptions)
admin.site.register(Plans)
