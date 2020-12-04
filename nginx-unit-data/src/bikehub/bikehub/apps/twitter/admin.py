from django.contrib import admin

from .models import FollowInfo, SearchKeyWord

# Register your models here.


class SearchKeyWordAdmin(admin.ModelAdmin):
    list_display = ('key_word', 'is_proccessing')
    readonly_fields = ('created_at', 'updated_at')


class FollowInfoAdmin(admin.ModelAdmin):
    list_display = ('twitter_user_id', 'is_followed', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(
    FollowInfo, FollowInfoAdmin
)

admin.site.register(
    SearchKeyWord, SearchKeyWordAdmin
)
