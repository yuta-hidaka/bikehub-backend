from django.contrib import admin
from .models import *

# Register your models here.


class MakerAdmin(admin.ModelAdmin):
    search_fields = [
        'maker_name_jp',
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
    Fc
)
admin.site.register(
    FcComment
)
