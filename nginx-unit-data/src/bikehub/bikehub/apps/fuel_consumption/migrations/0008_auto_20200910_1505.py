# Generated by Django 3.0.7 on 2020-09-10 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_consumption', '0007_auto_20200910_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fc',
            name='phot',
            field=models.ImageField(blank=True, default='', null=True, upload_to='uploads/'),
        ),
    ]
