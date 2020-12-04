from rest_framework import serializers
# from drf_queryfields import QueryFieldsMixin
from rest_framework.validators import UniqueTogetherValidator

from news.models import (MainCategoryTag, News, SourseSite, SubCategoryTag,
                         SubCategoryTagMap, TargetSite)


class TargetSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetSite
        fields = [
            'target_site_id',
            'is_there_another_source',
            'name',
        ]


class SourseSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourseSite
        fields = [
            'name',
            'sorse_url',
        ]


class SubCategoryTagMapSerializer(serializers.ModelSerializer):
    # news = NewsSerializer(read_only=True)

    class Meta:
        model = SubCategoryTagMap
        fields = [
            'sub_category_tag_map_id',
            'sub_category_tag',
            'news',
            'created_at',
            'updated_at',
        ]


class NewsSerializer(serializers.ModelSerializer):
    site = TargetSiteSerializer(read_only=True)
    source_site = SourseSiteSerializer(read_only=True)
    # subcategorys = serializers.SerializerMethodField()
    sub_category_tag_map = serializers.StringRelatedField(many=True)

    class Meta:
        model = News
        fields = [
            'news_id',
            'title',
            'summary',
            'url',
            'site',
            'featured_image',
            'sub_category_tag_map',
            'source_site',
            'created_at',
            'updated_at',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=News.objects.all(),
                fields=[
                    'news_id', 'sub_category_tag_map__sub_category_tag__main_category_tag_id'
                ]
            )
        ]


class MainCategoryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategoryTag
        fields = [
            'main_category_tag_id',
            'name',
            'is_active',
            'push_counter',
            'ordering_number',
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
