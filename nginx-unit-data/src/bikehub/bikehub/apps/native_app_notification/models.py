from django.db import models
import uuid

# Create your models here.
class PushNotificationSettings(models.Model):
    push_notification_settings_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    target_url = models.URLField(
        max_length=150,
        blank=True,
        default='div'
    )
    token = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )
    title = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'push_notification_settings'