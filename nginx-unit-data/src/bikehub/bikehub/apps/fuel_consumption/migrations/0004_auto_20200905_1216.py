# Generated by Django 3.0.7 on 2020-09-05 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_consumption', '0003_auto_20200830_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bike',
            name='fc_max_user_name',
        ),
        migrations.RemoveField(
            model_name='fc',
            name='user',
        ),
        migrations.RemoveField(
            model_name='fccomment',
            name='user',
        ),
    ]
