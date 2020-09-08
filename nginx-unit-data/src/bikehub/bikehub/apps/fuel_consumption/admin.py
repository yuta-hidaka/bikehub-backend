from django.contrib import admin
from .models import *

# Register your models here.


class MakerAdmin(admin.ModelAdmin):
    list_display = [
        'maker_id',
        'maker_name_jp',
        'created_at'
    ]
    search_fields = [
        'maker_id',
        'maker_name_jp',
    ]
    autocomplete_fields = [
        'country',
    ]


class FcAdmin(admin.ModelAdmin):
    list_display = [
        'fc_id',
        'fc',
        'user',
        'created_at'
    ]
    search_fields = [
        'fc_id',
        'user',
        'bike',
    ]
    autocomplete_fields = [
        'bike',
        'user',
    ]


class BikeAdmin(admin.ModelAdmin):
    list_display = [
        'bike_id',
        'bike_name',
        'maker',
        'created_at',
    ]
    search_fields = [
        'bike_name',
        'bike_id',
    ]
    autocomplete_fields = [
        'maker',
    ]


admin.site.register(
    Maker, MakerAdmin
)
admin.site.register(
    Country
)
admin.site.register(
    Eda
)
admin.site.register(
    Bike, BikeAdmin
)
admin.site.register(
    FuelType
)
admin.site.register(
    Fc, FcAdmin
)
admin.site.register(
    FcComment
)
