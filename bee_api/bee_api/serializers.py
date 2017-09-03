from rest_framework import serializers
from .models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('__all__')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('__all__')


class StateProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = State_Province
        fields = ('__all__')


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('__all__')


class HiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        fields = ('__all__')


class HiveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive_Data
        fields = ('__all__')
