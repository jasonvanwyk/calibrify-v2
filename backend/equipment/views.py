# ============================================================================
# File Path: backend/equipment/views.py
# Description: Views for equipment management system
# ============================================================================

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.utils import timezone
from .models import Equipment, Calibration, Maintenance
from .serializers import (
    EquipmentSerializer,
    CalibrationSerializer,
    MaintenanceSerializer,
)


class EquipmentFilter(filters.FilterSet):
    """Filter for Equipment model."""
    
    class Meta:
        model = Equipment
        fields = {
            'name': ['exact', 'icontains'],
            'serial_number': ['exact', 'icontains'],
            'category': ['exact', 'icontains'],
            'manufacturer': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
            'is_active': ['exact'],
            'last_calibration_date': ['exact', 'gt', 'lt'],
            'next_calibration_date': ['exact', 'gt', 'lt'],
        }


class CalibrationFilter(filters.FilterSet):
    """Filter for Calibration model."""
    
    class Meta:
        model = Calibration
        fields = {
            'equipment': ['exact'],
            'calibration_date': ['exact', 'gt', 'lt'],
            'calibrated_by': ['exact'],
            'calibration_standard': ['exact', 'icontains'],
            'measurement_point': ['exact', 'icontains'],
        }


class MaintenanceFilter(filters.FilterSet):
    """Filter for Maintenance model."""
    
    class Meta:
        model = Maintenance
        fields = {
            'equipment': ['exact'],
            'maintenance_date': ['exact', 'gt', 'lt'],
            'performed_by': ['exact'],
            'service_provider': ['exact', 'icontains'],
            'returned_to_production': ['exact'],
        }


class EquipmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Equipment model."""
    
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = EquipmentFilter
    search_fields = [
        'name',
        'serial_number',
        'category',
        'model_number',
        'manufacturer',
        'location',
    ]
    ordering_fields = [
        'name',
        'serial_number',
        'category',
        'manufacturer',
        'location',
        'last_calibration_date',
        'next_calibration_date',
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def dashboard_summary(self, request):
        """Get summary data for dashboard."""
        total_equipment = self.get_queryset().count()
        pending_calibrations = self.get_queryset().filter(
            next_calibration_date__lte=timezone.now().date()
        ).count()
        pending_maintenance = Maintenance.objects.filter(
            returned_to_production=False
        ).count()
        overdue_items = self.get_queryset().filter(
            next_calibration_date__lt=timezone.now().date()
        ).count()

        return Response({
            'total_equipment': total_equipment,
            'pending_calibrations': pending_calibrations,
            'pending_maintenance': pending_maintenance,
            'overdue_items': overdue_items,
        })


class CalibrationViewSet(viewsets.ModelViewSet):
    """ViewSet for Calibration model."""
    
    queryset = Calibration.objects.all()
    serializer_class = CalibrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = CalibrationFilter
    search_fields = [
        'equipment__name',
        'equipment__serial_number',
        'calibration_standard',
        'measurement_point',
    ]
    ordering_fields = [
        'calibration_date',
        'equipment__name',
        'calibrated_by__username',
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MaintenanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Maintenance model."""
    
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = MaintenanceFilter
    search_fields = [
        'equipment__name',
        'equipment__serial_number',
        'service_provider',
        'description',
    ]
    ordering_fields = [
        'maintenance_date',
        'equipment__name',
        'performed_by__username',
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
