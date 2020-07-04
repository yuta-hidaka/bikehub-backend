from django.db import models
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(
    TargetSite,
)

admin.site.register(
    Tag,
)

admin.site.register(
    News,
)

admin.site.register(
    TagMap
)
