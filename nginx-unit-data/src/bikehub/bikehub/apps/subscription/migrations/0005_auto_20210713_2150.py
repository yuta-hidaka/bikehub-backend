# Generated by Django 3.2.5 on 2021-07-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_auto_20210713_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='plans',
            name='publish_ads',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plans',
            name='publish_news',
            field=models.BooleanField(default=False),
        ),
    ]
