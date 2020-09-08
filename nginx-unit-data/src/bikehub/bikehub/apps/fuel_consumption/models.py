# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import CustomUser
import uuid


class Country(models.Model):
    country_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    country = models.CharField(
        max_length=120,
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
        return self.country

    class Meta:
        db_table = 'fc_country'


class Maker(models.Model):
    maker_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    maker_name_jp = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    maker_name_en = models.CharField(
        max_length=150,
        blank=True,
        default=''
    )
    country = models.ForeignKey(
        Country,
        default=None,
        blank=True,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.maker_name_jp

    class Meta:
        db_table = 'fc_maker'


class Eda(models.Model):
    eda_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    engine_displacement_area = models.CharField(
        max_length=120,
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
        return self.engine_displacement_area

    class Meta:
        db_table = 'fc_eda'


class Bike(models.Model):
    bike_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    bike_name = models.CharField(
        max_length=120,
        blank=True,
        default=''
    )

    phot = models.ImageField(
        upload_to='uploads/',
        null=True,
        default=None
    )

    fc_max = models.FloatField(
        null=True,
        default=None
    )

    fc_ave = models.FloatField(
        null=True,
        default=None
    )

    tag = models.CharField(
        max_length=1500,
        blank=True,
        default=''
    )

    fc_max_user_name = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )

    maker = models.ForeignKey(
        Maker,
        on_delete=models.CASCADE
    )

    engine_displacement_area = models.ForeignKey(
        Eda,
        on_delete=models.CASCADE
    )

    engine_displacement = models.IntegerField(
        null=True,
        default=None
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.bike_name

    class Meta:
        db_table = 'fc_bike'


class FuelType(models.Model):
    fuel_type_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    fuel = models.CharField(
        max_length=20,
        blank=True,
        default=''
    )

    def __str__(self):
        return self.fuel

    class Meta:
        db_table = 'fc_fuel_type'


class Fc(models.Model):
    fc_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    fc = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999)
        ]
    )

    distance_bf = models.FloatField(
        blank=True,
        null=True,
        default=0
    )

    distance_af = models.FloatField(
        blank=True,
        null=True,
        default=0
    )

    distance = models.FloatField(
        default=0
    )

    fc_user_official = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        default=''
    )

    phot_id = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        default=''
    )

    gas_amount = models.FloatField(
        blank=True,
        null=True,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)
        ]
    )

    city_ride = models.IntegerField(
        default=50,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )

    high_way_ride = models.IntegerField(
        default=50,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )

    fc_comment = models.TextField(
        max_length=2000,
        blank=True,
        default=''
    )

    fc_good = models.IntegerField(
        default=0
    )

    model_year = models.IntegerField(
        null=True,
        default=None
    )

    fuel_type = models.ForeignKey(
        FuelType,
        on_delete=models.CASCADE
    )

    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    phot = models.ImageField(
        upload_to='uploads/',
        blank=True,
        default=''
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return str(self.bike)

    class Meta:
        db_table = 'fc'


class FcComment(models.Model):
    fc_comment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    comment = models.TextField(
        default='',
        max_length=500
    )

    fc = models.ForeignKey(
        Fc,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'fc_commnet'
