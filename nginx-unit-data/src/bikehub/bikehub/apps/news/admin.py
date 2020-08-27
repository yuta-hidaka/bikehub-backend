from django.db import models
from django.contrib import admin
from .models import *

# Register your models here.


class TargetSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'rss_url', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


class MainCategoryTagAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]


class SubCategoryTagAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'tag_counter',
        'main_category_tag',
        'related_of_maker',
        'is_tag',
    ]
    list_editable = [
        'main_category_tag',
        'related_of_maker',
        'is_tag',
    ]
    search_fields = [
        'name',
        'main_category_tag',
        'related_of_maker'
    ]
    autocomplete_fields = [
        'main_category_tag',
        'related_of_maker'
    ]


admin.site.register(
    TargetSite, TargetSiteAdmin
)

admin.site.register(
    MainCategoryTag, MainCategoryTagAdmin
)

admin.site.register(
    ContentTag,
)

admin.site.register(
    SubCategoryTag, SubCategoryTagAdmin
)

admin.site.register(
    News,
)

admin.site.register(
    SubCategoryTagMap
)