import uuid

from company.models import Company
from django.db import models


class Capability(models.Model):
    capability_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=None)
    bike_register = models.IntegerField(default=0)
    company_register = models.IntegerField(default=0)

    def __str__(self):
        return self.company

    class Meta:
        db_table = 'capability'


class Plans(models.Model):
    plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    monthly_max_bike_register = models.IntegerField(default=0)
    max_company_register = models.IntegerField(default=0)
    publish_ads = models.BooleanField(default=False)
    publish_news = models.BooleanField(default=False)
    stripe_price_id = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plans'


class Status(models.Model):
    status_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reason = models.TextField()
    code = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason

    class Meta:
        db_table = 'status'


class Subscriptions(models.Model):
    subscription_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, default=None)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE,)
    stripe_customer_id = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, default=None)
    expire = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company} - {self.plan}'

    class Meta:
        db_table = 'subscriptions'
