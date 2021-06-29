import uuid

from django.db import models
from users.models import CustomUser


class Company(models.Model):
    PLANS = (
        (10, 'starter'),
        (20, 'pro'),
        (30, 'bussiness'),
    )
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.CharField(max_length=100, choices=PLANS)
    name = models.TextField()
    stripe_customer_id = models.TextField()
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    address = models.TextField()
    email = models.EmailField()
    phone = models.TextField()
    post_code = models.TextField()
    description = models.TextField()
    prefecture = models.TextField()
    url = models.TextField()
    is_child = models.BooleanField(
        default=False
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
    PERMISSIONS = (
        (10, 'admin'),
        (20, 'editor'),
        (30, 'viewr'),
    )
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
    permission = models.TextField(
        choices=PERMISSIONS
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
        db_table = 'Evaluation'