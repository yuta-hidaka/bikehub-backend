# Generated by Django 3.2.5 on 2021-07-15 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller', '0002_auto_20210715_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomments',
            name='product',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_comments', to='seller.products'),
        ),
        migrations.AlterField(
            model_name='productcomments',
            name='writer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
