from django.db import models
from django.contrib import admin
from .models import *

# Register your models here.


class TargetSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'rss_url', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


class MainCategoryTagAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'created_at',
        'is_active',
        'ordering_number',
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
        'main_category_tag__name',
        'related_of_maker__maker_name_jp',
        'main_category_tag',
        'related_of_maker'
    ]
    autocomplete_fields = [
        'main_category_tag',
        'related_of_maker'
    ]
    ordering = ['tag_counter']


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
