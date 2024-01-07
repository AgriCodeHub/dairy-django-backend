
from django.urls import path, include
from rest_framework import routers

from health.views import (
    WeightRecordViewSet,
    CullingRecordViewSet,
    QuarantineRecordViewSet,
    PathogenViewSet,
)

app_name = 'health'

router = routers.DefaultRouter()
router.register(r'weight-records', WeightRecordViewSet, basename='weight-records')
router.register(r'culling-records', CullingRecordViewSet, basename='culling-records')
router.register(r'quarantine-records', QuarantineRecordViewSet, basename='quarantine-records')
router.register(r'pathogens', PathogenViewSet, basename='pathogens')

urlpatterns = [
    path('', include(router.urls))
]
