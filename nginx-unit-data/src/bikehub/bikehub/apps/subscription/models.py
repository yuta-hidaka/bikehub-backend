import uuid

from django.db import models
from sell_bike.models import Company


class Plans(models.Model):
    plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    monthly_max_bike_register = models.IntegerField(default=0)
    max_company_register = models.IntegerField(default=0)
    publish_ads = models.TextField()
    publish_news = models.TextField()
    stripe_price_id = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'plans'


class Subscriptions(models.Model):
    subscription_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE,)
    stripe_customer_id = models.TextField()
    expired_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company} - {self.plan}'

    class Meta:
        db_table = 'subscriptions'
