from fuel_consumption.models import *
from rest_framework import serializers


# 著者
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
