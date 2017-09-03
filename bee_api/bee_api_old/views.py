from rest_framework import viewsets

from bee_api.bee_web.serializers import *


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class StateProvinceViewSet(viewsets.ModelViewSet):
    queryset = State_Province.objects.all()
    serializer_class = StateProvinceSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class HiveViewSet(viewsets.ModelViewSet):
    queryset = Hive.objects.all()
    serializer_class = HiveSerializer


class HiveDataViewSet(viewsets.ModelViewSet):
    queryset = Hive_Data.objects.all()
    serializer_class = HiveDataSerializer