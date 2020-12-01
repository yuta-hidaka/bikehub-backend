# Generated by Django 3.0.7 on 2020-12-01 12:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FollowInfo',
            fields=[
                ('follow_info_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('twitter_user_id', models.BigIntegerField(default=0)),
                ('is_followed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'follow_info',
            },
        ),
        migrations.CreateModel(
            name='SearchKeyWord',
            fields=[
                ('search_key_word_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key_word', models.CharField(blank=True, default='', max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('is_proccessing', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'search_key_word',
            },
        ),
    ]