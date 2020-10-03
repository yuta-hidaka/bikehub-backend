from django.db import models
import uuid

# Create your models here.


class PushNotificationSettings(models.Model):
    target_url = models.URLField(
        max_length=150,
        blank=True,
    )
    title = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'push_notification_settings'


class PushNotificationTokens(models.Model):
    push_notification_tokens_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    token = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )
    is_active = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.token)

    class Meta:
        db_table = 'push_notification_tokens'
        ordering = ['-created_at']
