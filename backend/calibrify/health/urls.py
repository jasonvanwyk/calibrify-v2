# ============================================================================
# File Path: backend/calibrify/health/urls.py
# Description: URL configuration for health checks
# ============================================================================

from django.urls import path
from . import views

app_name = 'health'

urlpatterns = [
    path('', views.health_check, name='health_check'),
] 