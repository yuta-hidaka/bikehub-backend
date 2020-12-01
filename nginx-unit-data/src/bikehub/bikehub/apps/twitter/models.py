import uuid

from django.db import models


class SearchKeyWord(models.Model):
    search_key_word_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    key_word = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    is_active = models.BooleanField(
        default=False
    )
    is_proccessing = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.key_word

    class Meta:
        db_table = 'search_key_word'


class FollowInfo(models.Model):
    follow_info_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    twitter_user_id = models.BigIntegerField(
        default=0
    )
    is_followed = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.twitter_user_id)

    class Meta:
        db_table = 'follow_info'
