from fuel_consumption.models import Maker, Country, Eda, Bike, fuelType, Fc, FcComment
from rest_framework import serializers


class MakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maker
        fields = [
            'id',
            'maker_name_jp',
            'maker_name_en',
            'country'
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id',
            'name'
        ]


class EdaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eda
        fields = [
            'id',
            'name'
        ]


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = [
            'id',
            'name'
        ]


class fuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = fuelType
        fields = [
            'id',
            'name'
        ]


class FcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fc
        fields = [
            'id',
            'name'
        ]


class FcCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcComment
        fields = [
            'id',
            'name'
        ]
