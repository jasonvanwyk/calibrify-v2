# ============================================================================
# File Path: backend/frontend/urls.py
# Description: URL configuration for frontend app
# ============================================================================

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'frontend'

urlpatterns = [
    # Dashboard as the main view
    path('', views.dashboard, name='dashboard'),
    
    # Equipment URLs
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    
    # Calibration URLs
    path('calibration/', views.calibration_list, name='calibration_list'),
    path('calibration/create/', views.calibration_create, name='calibration_create'),
    
    # Maintenance URLs
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/create/', views.maintenance_create, name='maintenance_create'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # Calendar
    path('calendar/', views.calendar, name='calendar'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_field_name='next'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] 