from rest_framework import generics
# views.py
from rest_framework_api_key.permissions import HasAPIKey
from rest.serializer.native_app_notification import PushNotificationTokensSerializer
from native_app_notification.models import PushNotificationTokens
from rest_framework.permissions import IsAdminUser


class PushNotificationTokensList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | HasAPIKey]
    queryset = PushNotificationTokens.objects.all()
    serializer_class = PushNotificationTokensSerializer
