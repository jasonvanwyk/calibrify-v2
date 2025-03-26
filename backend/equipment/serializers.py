# ============================================================================
# File Path: backend/equipment/serializers.py
# Description: Serializers for equipment management system
# ============================================================================

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Equipment, Calibration, Maintenance


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class CalibrationSerializer(serializers.ModelSerializer):
    """Serializer for Calibration model."""
    
    calibrated_by = UserSerializer(read_only=True)
    certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = Calibration
        fields = (
            'id',
            'equipment',
            'calibration_date',
            'calibrated_by',
            'calibration_standard',
            'measurement_point',
            'results',
            'notes',
            'certificate_file',
            'certificate_url',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_certificate_url(self, obj):
        if obj.certificate_file:
            return self.context['request'].build_absolute_uri(
                obj.certificate_file.url
            )
        return None


class MaintenanceSerializer(serializers.ModelSerializer):
    """Serializer for Maintenance model."""
    
    performed_by = UserSerializer(read_only=True)
    certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = (
            'id',
            'equipment',
            'maintenance_date',
            'performed_by',
            'service_provider',
            'description',
            'returned_to_production',
            'notes',
            'certificate_file',
            'certificate_url',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_certificate_url(self, obj):
        if obj.certificate_file:
            return self.context['request'].build_absolute_uri(
                obj.certificate_file.url
            )
        return None


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for Equipment model."""
    
    created_by = UserSerializer(read_only=True)
    calibrations = CalibrationSerializer(many=True, read_only=True)
    maintenance_records = MaintenanceSerializer(many=True, read_only=True)
    pending_calibrations = serializers.SerializerMethodField()
    pending_maintenance = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = (
            'id',
            'name',
            'serial_number',
            'category',
            'purchase_date',
            'model_number',
            'manufacturer',
            'location',
            'calibration_interval_type',
            'calibration_interval_value',
            'notes',
            'created_by',
            'created_at',
            'updated_at',
            'last_calibration_date',
            'next_calibration_date',
            'is_active',
            'calibrations',
            'maintenance_records',
            'pending_calibrations',
            'pending_maintenance',
        )
        read_only_fields = (
            'created_at',
            'updated_at',
            'last_calibration_date',
            'next_calibration_date',
        )

    def get_pending_calibrations(self, obj):
        """Get count of pending calibrations."""
        if not obj.next_calibration_date:
            return 0
        from django.utils import timezone
        today = timezone.now().date()
        if obj.next_calibration_date <= today:
            return 1
        return 0

    def get_pending_maintenance(self, obj):
        """Get count of pending maintenance records."""
        return obj.maintenance_records.filter(
            returned_to_production=False
        ).count() 