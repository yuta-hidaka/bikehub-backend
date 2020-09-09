from fuel_consumption.models import Maker, Country, Eda, Bike, FuelType, Fc, FcComment
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country(read_only=True)
        fields = [
            'country_id',
            'country',
            'created_at',
            'updated_at',
        ]


class MakerSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Maker
        fields = [
            'maker_id',
            'maker_name_jp',
            'maker_name_en',
            'country',
            'created_at',
            'updated_at',
        ]


class EdaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eda
        fields = [
            'eda_id',
            'engine_displacement_area',
            'created_at',
            'updated_at',
        ]


class BikeSerializer(serializers.ModelSerializer):
    maker = MakerSerializer(read_only=True)

    class Meta:
        model = Bike
        fields = [
            'bike_id',
            'bike_name',
            'phot',
            'fc_max',
            'fc_ave',
            'tag',
            'fc_max_user_name',
            'maker',
            'country',
            'engine_displacement_area',
            'engine_displacement',
            'created_at',
            'created_at',
            'updated_at',
        ]


class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = [
            'fuel_type_id',
            'fuel',
            'created_at',
            'updated_at',
        ]


class FcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fc
        fields = [
            # 'fc_id',
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
            'updated_at',
        ]


class FcCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcComment
        fields = [
            'fc_comment_id',
            'comment',
            'fc',
            'user',
            'created_at',
            'updated_at',
        ]
