# Generated by Django 3.2.5 on 2021-07-13 12:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        ('subscription', '0002_rename_expired_at_subscriptions_expire'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capability',
            fields=[
                ('capability_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bike_register', models.IntegerField(default=0)),
                ('company_register', models.IntegerField(default=0)),
                ('company', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
            options={
                'db_table': 'capability',
            },
        ),
    ]