# Generated by Django 3.2.5 on 2021-07-12 13:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('plan_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('monthly_max_bike_register', models.IntegerField(default=0)),
                ('max_company_register', models.IntegerField(default=0)),
                ('publish_ads', models.TextField()),
                ('publish_news', models.TextField()),
                ('stripe_price_id', models.TextField()),
            ],
            options={
                'db_table': 'plans',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reason', models.TextField()),
                ('code', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'status',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('subscription_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('stripe_customer_id', models.TextField()),
                ('expired_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.plans')),
                ('status', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='subscription.status')),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
    ]
