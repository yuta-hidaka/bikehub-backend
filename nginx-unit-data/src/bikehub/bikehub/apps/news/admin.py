from django.contrib import admin
from django.db import models

from .models import (ContentTag, MainCategoryTag, News, SourseSite,
                     SubCategoryTag, SubCategoryTagMap, TargetSite)


class TargetSiteAdmin(admin.ModelAdmin):
    list_editable = ('deactive',)
    list_display = ('name', 'deactive', 'rss_url', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


class SourseSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'sorce_url')
    readonly_fields = ('created_at', 'updated_at')


class MainCategoryTagAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created_at',
        'is_active',
        'ordering_number',
        'push_counter',
    ]
    search_fields = [
        'name',
    ]
    list_editable = [
        'is_active',
        'ordering_number',
    ]
    ordering = ['ordering_number']


class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'created_at',
        'site'
    ]
    search_fields = [
        'title',
        'summary'
    ]
    ordering = ['-created_at']


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
        # 'main_category_tag',
        # 'related_of_maker'
    ]
    autocomplete_fields = [
        'main_category_tag',
        'related_of_maker'
    ]
    ordering = ['tag_counter']


admin.site.register(
    SourseSite, SourseSiteAdmin
)

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
    News, NewsAdmin
)

admin.site.register(
    SubCategoryTagMap
)
