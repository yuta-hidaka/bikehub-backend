import uuid

from django.db import models
from django.db.models.deletion import CASCADE
from django_resized import ResizedImageField
from users.models import CustomUser


class Company(models.Model):
    def get_upload_path(obj, _):
        return f'media/company/{obj.company_id}/featured_image/'

    def get_thumbnail_upload_path(obj, _):
        return f'media/company/{obj.company_id}/thumbnail_image/'

    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    email = models.EmailField(unique=True)
    phone = models.TextField()
    post_code = models.TextField()
    description = models.TextField()
    prefecture = models.TextField(default='')
    city = models.TextField(default='')
    street = models.TextField(default='')
    building = models.TextField(default='')
    url = models.TextField()
    active = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        CustomUser, related_name='company_created_by', on_delete=CASCADE, default=None, null=True)
    updated_by = models.ForeignKey(
        CustomUser, related_name='company_updated_by', on_delete=CASCADE, default=None, null=True)
    owned_featured_image = ResizedImageField(
        quality=75,
        upload_to=get_upload_path,
        null=True,
        blank=True,
        default=None
    )
    thumbnail_image = ResizedImageField(
        size=[320, 180],
        quality=20,
        upload_to=get_thumbnail_upload_path,
        null=True,
        blank=True,
        default=None
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'


class CompanyGroup(models.Model):
    company_group_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    child = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='child_company',
    )
    parent = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='parent_company',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_group_id

    class Meta:
        db_table = 'company_group'


class CompanyUserGroup(models.Model):
    class Permissions(models.IntegerChoices):
        ADMIN = 10, 'admin'
        EDITOR = 20, 'editor'
        VIEWER = 30, 'viewer'
    company_group_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    permission = models.IntegerField(
        choices=Permissions.choices,
        default=Permissions.VIEWER
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.company} - {self.user}'

    class Meta:
        db_table = 'company_user_group'


class Evaluation(models.Model):
    STARS = (
        (5, '★★★★★'),
        (4, '★★★★'),
        (3, '★★★'),
        (2, '★★'),
        (1, '★'),
    )
    evaluation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    star = models.TextField(
        choices=STARS
    )
    description = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.company} - {self.user}'

    class Meta:
        db_table = 'evaluation'
