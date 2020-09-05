from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
# from fuel_consumption.models import Bike
# from news.models import News


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    disp_name = models.CharField(
        max_length=50, blank=True, default='', verbose_name=u'表示名',
    )
    birthday = models.DateField(
        null=True, default=None
    )
    gender = models.IntegerField(
        default=0
    )
    # 自由入力で自分のバイクを保存
    ubike1 = models.CharField(
        max_length=150, blank=True, default=''
    )
    ubike2 = models.CharField(
        max_length=150, blank=True, default=''
    )
    # 外部参照から自分のバイクを取得
    # ubike1_by_list = models.ForeignKey(
    #     "Bike",
    #     on_delete=models.CASCADE,
    #     null=True,
    #     default=None,
    #     blank=True
    # )
    # ubike2_by_list = models.ForeignKey(
    #     "Bike",
    #     on_delete=models.CASCADE,
    #     null=True,
    #     default=None,
    #     blank=True
    # )
    accept = models.BooleanField(
        default=False
    )
    login_date = models.DateTimeField(
        null=True, default=None
    )
    login_cnt = models.IntegerField(
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    # USERNAME_FIELD = 'email'
    # this field means that when you try to sign in the username field will be the email
    # change it to whatever you want django to see as the username when authenticating the user
    REQUIRED_FIELDS = ['disp_name', 'accept', ]

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザー一覧'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.email

    def has_module_perms(self, app_label):
        return True
