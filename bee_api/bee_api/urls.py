
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from .views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register("countries", CountryViewSet)
router.register("locations", LocationViewSet)
router.register("state-provinces", StateProvinceViewSet)
router.register("owners", OwnerViewSet)
router.register("hives", HiveViewSet)
router.register("hivedatas", HiveDataViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
