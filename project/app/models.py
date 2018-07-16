# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area'

    def __str__(self):
        return self.name


class Collect(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, primary_key=True)
    house = models.ForeignKey('House', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'collect'
        unique_together = (('user', 'house'),)

# class Collect(models.Model):
#     user = models.ForeignKey('User', models.DO_NOTHING, primary_key=True)
#     house = models.ForeignKey('House', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'collect'
#         unique_together = (('user', 'house'),)


class Count(models.Model):
    count_id = models.AutoField(primary_key=True)
    house = models.ForeignKey('House', models.DO_NOTHING, blank=True, null=True)
    look_times = models.IntegerField(blank=True, null=True)
    area_look_times = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'count'


class House(models.Model):
    house_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    area = models.ForeignKey(Area, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('HouseType', models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    acreage = models.IntegerField(blank=True, null=True)
    index_img_url = models.CharField(max_length=1024, blank=True, null=True)
    house_status = models.CharField(max_length=10, null=True)
    col_user = models.ManyToManyField('User', through='Collect', related_name='col_house')


    class Meta:
        managed = False
        db_table = 'house'


class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=128, blank=True, null=True)
    css = models.CharField(max_length=512, blank=True, null=True)
    houses = models.ManyToManyField(House, through='HouseFacility')

    class Meta:
        managed = False
        db_table = 'facility'


class HouseFacility(models.Model):
    facility = models.ForeignKey(Facility, models.DO_NOTHING, primary_key=True)
    house = models.ForeignKey(House, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'house_facility'

        unique_together = (('facility', 'house'),)



class HouseDetail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    house = models.ForeignKey(House, models.DO_NOTHING, blank=True, null=True)
    lease = models.CharField(max_length=512, blank=True, null=True)
    pay_way = models.CharField(max_length=512, blank=True, null=True)
    floor = models.CharField(max_length=512, blank=True, null=True)
    house_head = models.CharField(max_length=128, blank=True, null=True)
    community = models.CharField(max_length=512, blank=True, null=True)
    surround_facility = models.CharField(max_length=1024, blank=True, null=True)
    transportation = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'house_detail'


class HouseImg(models.Model):
    img_id = models.AutoField(primary_key=True)
    house = models.ForeignKey(House, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'house_img'


class HouseType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'house_type'

    def __str__(self):
        return self.type_name


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    vip = models.IntegerField(blank=True, null=True)
    admin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)
    account = models.CharField(unique=True, max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128,blank=True, null=True)
    nick_name = models.CharField(max_length=128, blank=True, null=True)
    avatar = models.ImageField(upload_to='icon', blank=True, null=True)
    id_name = models.CharField(max_length=64, blank=True, null=True)
    id_card = models.CharField(max_length=64, blank=True, null=True)
    ticket = models.CharField(max_length=255, blank=True, null=True)
    out_time = models.DateTimeField()


    class Meta:
        managed = False
        db_table = 'user'


class Forbidden(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'forbidden'
