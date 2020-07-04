from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    disp_name = models.CharField(
        max_length=50, blank=True, default='', verbose_name=u'表示名',)
    birthday = models.DateField(null=True, default=None)
    gender = models.IntegerField(default=0)
    # 自由入力で自分のバイクを保存
    ubike1 = models.CharField(max_length=150, blank=True, default='')
    ubike2 = models.CharField(max_length=150, blank=True, default='')
    # 外部参照から自分のバイクを取得
    ubike1_by_list = models.CharField(max_length=150, blank=True, default='')
    ubike2_by_list = models.CharField(max_length=150, blank=True, default='')
    accept = models.BooleanField(default=False)
    login_date = models.DateField(null=True, default=None)
    login_cnt = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザー一覧'

    def __str__(self):
        return self.email
