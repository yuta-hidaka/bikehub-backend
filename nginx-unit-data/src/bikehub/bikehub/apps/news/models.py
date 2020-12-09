import uuid

from django.db import models
from fuel_consumption.models import Maker

# Create your models here.


class ContentTag(models.Model):
    content_tag_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    tag_type = models.CharField(
        max_length=150,
        blank=True,
        default='div'
    )
    tag_id_name = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )
    tag_class_name = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )

    def __str__(self):
        return (
            str(self.tag_type)
            + ', id= ' + str(self.tag_id_name)
            + ', class= ' + str(self.tag_class_name)
        )

    class Meta:
        db_table = 'news_content_tag'


class TargetSite(models.Model):
    target_site_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    rss_url = models.URLField(
        default=''
    )
    url = models.URLField(
        blank=True,
        default=''
    )
    content_tag = models.ForeignKey(
        ContentTag,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=False
    )
    deactive = models.BooleanField(
        default=False
    )
    is_there_another_source = models.BooleanField(
        default=False
    )
    reason = models.TextField(
        blank=True,
        default=''
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'news_target_site'


class MainCategoryTag(models.Model):
    main_category_tag_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    is_active = models.BooleanField(
        default=False
    )
    ordering_number = models.IntegerField(
        default=0
    )
    push_counter = models.IntegerField(
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'news_main_category_tag'


class SubCategoryTag(models.Model):
    sub_category_tag_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    main_category_tag = models.ForeignKey(
        MainCategoryTag,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True,
        related_name='sub_category_tag'
    )
    related_of_maker = models.ForeignKey(
        Maker,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True,
        related_name='sub_category_tag'
    )
    tag_counter = models.IntegerField(
        blank=True,
        default=0
    )
    is_tag = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'news_sub_category_tag'
        ordering = (
            '-tag_counter',
            '-main_category_tag',
        )


class SourseSite(models.Model):
    source_site_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    sorce_url = models.URLField(
        default=''
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'source_site'
        ordering = (
            'created_at',
        )


class News(models.Model):
    news_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    summary = models.TextField(
        blank=True,
        default=''
    )
    url = models.URLField(
        default=''
    )
    site = models.ForeignKey(
        TargetSite,
        on_delete=models.CASCADE
    )
    source_site = models.ForeignKey(
        SourseSite,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    featured_image = models.URLField(
        max_length=500
    )
    owned_featured_image = models.ImageField(
        upload_to='media/news/featured_image/',
        null=True,
        blank=True,
        default=None
    )
    is_posted = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'news'


class SubCategoryTagMap(models.Model):
    sub_category_tag_map_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sub_category_tag = models.ForeignKey(
        SubCategoryTag,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
        null=True,
        related_name='sub_category_tag_map'
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='sub_category_tag_map'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.sub_category_tag)

    class Meta:
        db_table = 'news_sub_category_tag_map'
