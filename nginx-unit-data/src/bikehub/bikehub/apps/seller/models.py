import uuid

from company.models import Company
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from fuel_consumption.models import Bike
from users.models import CustomUser


class Products(models.Model):
    class Product(models.TextChoices):
        MOTO = 'MOTO', _('MotorBike')

    class Color(models.TextChoices):
        GREEN = '#2DC200', _('GREEN')
        RED = '#F2340A', _('ED')
        YELLOW = '#FFFE02', _('YELLOW')
        SILVER = '#E5E5E5', _('SILVER')
        WHITE = '#FFFFFF', _('WHITE')
        BLACK = '#000000', _('BLACK')
        PINK = '#FB9AFF', _('PINK')
        BLUE = '#015CFF', _('BLUE')
        GRAY = '#9E9E9E', _('GRAY')
        ANOTHER = '', _('ANOTHER')
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.CharField(max_length=5, choices=Product.choices, default=Product.MOTO)
    color = models.CharField(max_length=10, choices=Color.choices, default=Color.ANOTHER)
    company = models.ForeignKey(Company, on_delete=CASCADE, default=None, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=CASCADE, default=None, null=True)
    moto = models.ForeignKey(Bike, on_delete=CASCADE)
    title = models.TextField()
    description = models.TextField()
    price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    model_year = models.IntegerField(default=0)
    vehicle_inspection = models.DateField()
    mileage = models.IntegerField(default=0)
    displacement = models.IntegerField(default=0)
    electric_power = models.IntegerField(default=0)
    # flg
    custom = models.BooleanField(default=False)
    abs = models.BooleanField(default=False)
    sel_on_web = models.BooleanField(default=False)
    led = models.BooleanField(default=False)
    maker_warranty = models.BooleanField(default=False)
    seller_warranty = models.BooleanField(default=False)
    etc = models.BooleanField(default=False)
    navigation = models.BooleanField(default=False)
    fi = models.BooleanField(default=False)
    four_storoke = models.BooleanField(default=False)
    mt = models.BooleanField(default=False)
    reimport = models.BooleanField(default=False)
    repaired = models.BooleanField(default=False)
    free_oil_change = models.BooleanField(default=False)
    free_maintenance = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    electric_bike = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.moto

    class Meta:
        db_table = 'products'


class ProductImages(models.Model):
    def get_upload_path(obj, _):
        return f'media/product/{obj.product.product_id}/featured_image/'

    def get_thumbnail_upload_path(obj, _):
        return f'media/product/{obj.product.product_id}/thumbnail_image/'

    product_image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, related_name='images', on_delete=CASCADE, null=True)
    owned_featured_image = ResizedImageField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        default=None
    )
    thumbnail_image = ResizedImageField(
        size=[320, 180],
        upload_to=get_thumbnail_upload_path,
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return self.product

    class Meta:
        db_table = 'product_images'


class ProductComments(models.Model):
    product_comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    product = models.ForeignKey(Products, related_name='comments', on_delete=CASCADE, null=True, default=None)
    writer = models.ForeignKey(CustomUser, related_name='user', on_delete=CASCADE, null=True, default=None)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'product_comments'
