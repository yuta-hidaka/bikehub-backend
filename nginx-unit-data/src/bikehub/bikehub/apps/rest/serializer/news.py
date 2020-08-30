from news.models import News, MainCategoryTag, SubCategoryTag, SubCategoryTagMap,TargetSite
from rest_framework import serializers
# from drf_queryfields import QueryFieldsMixin


class NewsSerializer(serializers.ModelSerializer):
    site=TargetSiteSerializer(read_only=True)
    class Meta:
        model = News
        fields = [
            'news_id',
            'title',
            'summary',
            'url',
            'site',
            'featured_image',
            'created_at',
            'updated_at',
        ]

class TargetSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetSite
        fields = [
            'target_site_id',
            'name',
        ]


class MainCategoryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategoryTag
        fields = [
            'main_category_tag_id',
            'name',
            'created_at',
            'updated_at',
        ]


class SubCategoryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryTag
        fields = [
            'sub_category_tag_id',
            'name',
            'main_category_tag',
            'related_of_maker',
            'created_at',
            'updated_at',
        ]


class SubCategoryTagMapSerializer(serializers.ModelSerializer):
    news = NewsSerializer(read_only=True)

    class Meta:
        model = SubCategoryTagMap
        fields = [
            'sub_category_tag_map_id',
            'sub_category_tag',
            'news',
            'created_at',
            'updated_at',
        ]
