# Generated by Django 3.0.7 on 2020-06-30 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetsite',
            name='url',
            field=models.URLField(blank=True, default=''),
        ),
    ]
