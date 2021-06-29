from django.contrib import admin

from sell_bike.models import Company, CompanyGroup, CompanyUserGroup, Evaluation

# Register your models here.


admin.site.register(Company)
admin.site.register(CompanyGroup)
admin.site.register(CompanyUserGroup)
admin.site.register(Evaluation)
