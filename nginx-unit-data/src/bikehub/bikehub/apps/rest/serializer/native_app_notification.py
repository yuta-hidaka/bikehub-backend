from native_app_notification.models import PushNotificationTokens
from rest_framework import serializers
# from drf_queryfields import QueryFieldsMixin



class PushNotificationTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotificationTokens
        fields = [
            'token',
            'is_active',
        ]

    def create(self, validated_data):
        token, created = PushNotificationTokens.objects.get_or_create(
            token=validated_data['token'],
            defaults={
                'is_active': False,
            })
        return token
