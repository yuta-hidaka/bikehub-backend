from django.db import models
from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(TargetSite)
class TargetSiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rss_url', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(
    MainCategoryTag,
)

admin.site.register(
    ContentTag,
)

admin.site.register(
    SubCategoryTag,
)

admin.site.register(
    News,
)

admin.site.register(
    SubCategoryTagMap
)
