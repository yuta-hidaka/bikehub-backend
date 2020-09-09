# Generated by Django 3.0.7 on 2020-09-08 09:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_consumption', '0005_auto_20200905_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='fc',
            name='distance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='fc',
            name='distance_af',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='fc',
            name='distance_bf',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='fc',
            name='gas_amount',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]