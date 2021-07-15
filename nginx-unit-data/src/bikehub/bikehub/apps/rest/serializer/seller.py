from rest.serializer.company import CompanySerializer
from rest.serializer.fuel_consumption import BikeSerializer
from rest.serializer.users import UserReadonlySerializer
from rest_framework import serializers

from fuel_consumption.models import (Bike, Country, Eda, Fc, FcComment,
                                     FuelType, Maker)
from seller.models import ProductComments, ProductImages, Products


class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = [
            'product_image_id',
            'product',
            'owned_featured_image',
            'thumbnail_image',
            'created_at',
            'updated_at',
        ]


class ProductCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductComments
        fields = [
            'product_comment_id',
            'comment',
            'product',
            'writer',
            'created_at',
            'updated_at',
        ]


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = [
            'product_id',
            'product',
            'color',
            'company',
            'created_by',
            'moto',
            'title',
            'description',
            'price',
            'total_price',
            'model_year',
            'vehicle_inspection',
            'mileage',
            'displacement',
            'electric_power',
            'custom',
            'abs',
            'sel_on_web',
            'led',
            'maker_warranty',
            'seller_warranty',
            'etc',
            'navigation',
            'fi',
            'four_storoke',
            'mt',
            'reimport',
            'repaired',
            'free_oil_change',
            'free_maintenance',
            'security',
            'electric_bike',
            'images',
            'comments',
            'created_at',
            'updated_at',
        ]


class ProductsSerializerRead(serializers.ModelSerializer):
    created_by = UserReadonlySerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    moto = BikeSerializer(read_only=True)
    images = serializers.PrimaryKeyRelatedField(allow_null=True, many=True, queryset=ProductImages.objects.all())
    comments = serializers.PrimaryKeyRelatedField(allow_null=True, many=True, queryset=ProductComments.objects.all())

    class Meta:
        model = Products
        fields = [
            'product_id',
            'product',
            'color',
            'company',
            'created_by',
            'moto',
            'title',
            'description',
            'price',
            'total_price',
            'model_year',
            'vehicle_inspection',
            'mileage',
            'displacement',
            'electric_power',
            'custom',
            'abs',
            'sel_on_web',
            'led',
            'maker_warranty',
            'seller_warranty',
            'etc',
            'navigation',
            'fi',
            'four_storoke',
            'mt',
            'reimport',
            'repaired',
            'free_oil_change',
            'free_maintenance',
            'security',
            'electric_bike',
            'images',
            'comments',
            'created_at',
            'updated_at',
        ]
