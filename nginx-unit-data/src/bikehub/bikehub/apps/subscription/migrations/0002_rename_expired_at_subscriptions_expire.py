# Generated by Django 3.2.5 on 2021-07-12 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriptions',
            old_name='expired_at',
            new_name='expire',
        ),
    ]