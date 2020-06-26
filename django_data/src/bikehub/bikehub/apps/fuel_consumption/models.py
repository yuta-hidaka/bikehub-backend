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


class Maker(models.Model):
    maker_name_jp = models.CharField(max_length=150, blank=True, default='')
    maker_name_en = models.CharField(max_length=150, blank=True, default='')
    country_id = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.maker_name_jp

    class Meta:
        db_table = 'm_maker'


class Country(models.Model):
    country = models.CharField(max_length=120, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

    class Meta:
        db_table = 'm_country'


class Eda(models.Model):
    engine_displacement_area = models.CharField(
        max_length=120, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.engine_displacement_area

    class Meta:
        db_table = 'm_eda'


class Bike(models.Model):
    bike_name = models.CharField(max_length=120, blank=True, default='')
    phot = models.ImageField(upload_to='uploads/')
    fc_max = models.FloatField(null=True, default=None)
    fc_ave = models.FloatField(null=True, default=None)
    tag = models.CharField(max_length=1500, blank=True, default='')
    fc_max_user_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    engine_displacement_area = models.ForeignKey(Eda, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bike_name

    class Meta:
        db_table = 'm_bike'


class fuelType(models.Model):
    fuel = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.bike_name

    class Meta:
        db_table = 'm_fuel_type'


class Fc(models.Model):
    fc = models.FloatField(default=0)
    distance_bf = models.FloatField(default=0)
    distance_af = models.FloatField(default=0)
    gas_amount = models.FloatField(
        default=0, validators=[MinValueValidator(1800), MaxValueValidator(9999)])
    city_ride = models.IntegerField(
        default=50, validators=[MinValueValidator(1), MaxValueValidator(100)])
    high_way_ride = models.IntegerField(
        default=50, validators=[MinValueValidator(1), MaxValueValidator(100)])
    fc_comment = models.CharField(max_length=2000, blank=True, default='')
    fc_good = models.IntegerField(default=0)
    model_year = models.IntegerField(null=True, default=None)
    fuel_type = models.ForeignKey(fuelType, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phot = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fc

    class Meta:
        db_table = 't_fc'


class FcComment(models.Model):
    comment = models.TextField(default='', max_length=500)
    fc = models.ForeignKey(Fc, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fc

    class Meta:
        db_table = 't_fc_commnet'
