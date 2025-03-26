# ============================================================================
# File Path: backend/equipment/urls.py
# Description: URL configuration for equipment app
# ============================================================================

from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    # Equipment endpoints
    path('equipment/', views.EquipmentListView.as_view(), name='equipment-list'),
    path('equipment/<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment-detail'),
    
    # Calibration endpoints
    path('calibrations/', views.CalibrationListView.as_view(), name='calibration-list'),
    path('calibrations/<int:pk>/', views.CalibrationDetailView.as_view(), name='calibration-detail'),
    
    # Maintenance endpoints
    path('maintenance/', views.MaintenanceListView.as_view(), name='maintenance-list'),
    path('maintenance/<int:pk>/', views.MaintenanceDetailView.as_view(), name='maintenance-detail'),
] 