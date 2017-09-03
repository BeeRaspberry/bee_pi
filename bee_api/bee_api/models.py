from __future__ import unicode_literals
import datetime
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200)


class State_Province(models.Model):
    country = models.ForeignKey('Country')
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10)

    def __repr__(self):
        return self.name


class Location(models.Model):
    street_addr = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state_province = models.ForeignKey('State_Province')


class Owner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passwd = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    location = models.ForeignKey('Location')

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Hive(models.Model):
    owner = models.ForeignKey('Owner')
# Hive location may differ from the location of the bee keeper
    location = models.ForeignKey('Location')
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
#    door_open = Column(Boolean, server_default=True)


class Hive_Data(models.Model):
    hive = models.ForeignKey('Hive')
    date_created = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5,decimal_places=2)
    humidity = models.DecimalField(max_digits=5,decimal_places=2)
#    door_open = Column(Boolean, server_default=True)
