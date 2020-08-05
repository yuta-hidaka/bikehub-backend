from fuel_consumption.models import Maker, Country, Eda, Bike, FuelType, Fc, FcComment
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id',
            'country'
        ]


class MakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maker
        fields = [
            'id',
            'maker_name_jp',
            'maker_name_en',
            'country'
        ]


class EdaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eda
        fields = [
            'id',
            'engine_displacement_area'
        ]


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = [
            'bike_name',
            'phot',
            'fc_max',
            'fc_ave',
            'tag',
            'fc_max_user_name',
            'maker',
            'engine_displacement_area',
            'engine_displacement',
            'created_at',
        ]


class fuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = fuelType
        fields = [
            'id',
            'fuel'
        ]


class FcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fc
        fields = [
            'id',
            'fc',
            'distance_bf',
            'distance_af',
            'fc_user_official',
            'phot_id',
            'gas_amount',
            'city_ride',
            'high_way_ride',
            'fc_comment',
            'fc_good',
            'model_year',
            'fuel_type',
            'bike',
            'user',
            'phot',
            'created_at',
        ]


class FcCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcComment
        fields = [
            'id',
            'comment',
            'fc',
            'user',
            'created_at'
        ]
