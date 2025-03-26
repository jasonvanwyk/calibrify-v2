# ============================================================================
# File Path: backend/equipment/urls.py
# Description: URL configuration for equipment app
# ============================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'equipment'

router = DefaultRouter()
router.register(r'equipment', views.EquipmentViewSet, basename='equipment')
router.register(r'calibrations', views.CalibrationViewSet, basename='calibration')
router.register(r'maintenance', views.MaintenanceViewSet, basename='maintenance')

urlpatterns = [
    path('', include(router.urls)),
] 