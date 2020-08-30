from django.contrib import admin
from .models import *

# Register your models here.


class MakerAdmin(admin.ModelAdmin):
    search_fields = [
        'maker_name_jp',
    ]
class FcAdmin(admin.ModelAdmin):
    list_display = [
        'fc',
        'user',
        'created_at'
    ]   
    search_fields = [
        'fc_id',
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
    Bike
)
admin.site.register(
    FuelType
)
admin.site.register(
    Fc,FcAdmin
)
admin.site.register(
    FcComment
)
