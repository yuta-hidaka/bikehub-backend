from news.models import News, MainCategoryTag, SubCategoryTag, SubCategoryTagMap
from rest_framework import serializers
# from drf_queryfields import QueryFieldsMixin


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'summary',
            'url',
            'site',
            'featured_image'
        ]


class MainCategoryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategoryTag
        fields = [
            'id',
            'name'
        ]


class SubCategoryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryTag
        fields = [
            'id',
            'name',
            'main_category_tag',
            'related_of_maker'
        ]


class SubCategoryTagMapSerializer(serializers.ModelSerializer):
    news = NewsSerializer(read_only=True)

    class Meta:
        model = SubCategoryTagMap
        fields = [
            'id',
            'sub_category_tag',
            'news'
        ]
