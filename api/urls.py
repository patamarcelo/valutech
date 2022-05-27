
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include

from .views import ValuRiskViewSet

router = routers.DefaultRouter()
router.register('valutech', ValuRiskViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
