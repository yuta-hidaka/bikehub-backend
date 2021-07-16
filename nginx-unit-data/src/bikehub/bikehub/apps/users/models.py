import uuid

from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_pk_to_url_str
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# from fuel_consumption.models import Bike
# from news.models import News


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def invite_user_to_company(self, email, **extra_fields):
        password = str(uuid.uuid4())
        self.create_user(email, password, **extra_fields)

    def invite_user(self, email, **extra_fields):
        password = str(uuid.uuid4())
        user = self.create_user(email, password, **extra_fields)
        token_generator = EmailAwarePasswordResetTokenGenerator()
        temp_key = token_generator.make_token(user)
        path = reverse("account_reset_password_from_key",
                       kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key))

        print(path.replace('auth', 'auth/seller'))

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, ** extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    # this field means that when you try to sign in the username field will be the email
    # change it to whatever you want django to see as the username when authenticating the user
    REQUIRED_FIELDS = ['disp_name', 'accept']
    objects = CustomUserManager()

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    disp_name = models.CharField(
        max_length=50, blank=True, default='', verbose_name=u'表示名',
    )
    # birthday = models.DateField(
    #     null=True, default=None
    # )
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
    seller = models.BooleanField(
        default=False
    )
    first_name = models.TextField()
    last_name = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザー一覧'

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.email

    # def has_module_perms(self, app_label):
    #     return True
