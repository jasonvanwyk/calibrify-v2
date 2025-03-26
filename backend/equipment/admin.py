# ============================================================================
# File Path: backend/equipment/admin.py
# Description: Admin interface configuration for equipment models
# ============================================================================

from django.contrib import admin
from .models import Equipment, Calibration, Maintenance


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'serial_number',
        'category',
        'manufacturer',
        'location',
        'last_calibration_date',
        'next_calibration_date',
        'is_active',
    )
    list_filter = (
        'category',
        'manufacturer',
        'is_active',
    )
    search_fields = (
        'name',
        'serial_number',
        'model_number',
        'manufacturer',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'last_calibration_date',
        'next_calibration_date',
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'serial_number',
                'category',
                'purchase_date',
                'model_number',
                'manufacturer',
                'location',
            )
        }),
        ('Calibration Settings', {
            'fields': (
                'calibration_interval_type',
                'calibration_interval_value',
                'last_calibration_date',
                'next_calibration_date',
            )
        }),
        ('Additional Information', {
            'fields': (
                'notes',
                'is_active',
            )
        }),
        ('System Information', {
            'fields': (
                'created_by',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Calibration)
class CalibrationAdmin(admin.ModelAdmin):
    list_display = (
        'equipment',
        'calibration_date',
        'calibrated_by',
        'calibration_standard',
        'measurement_point',
    )
    list_filter = (
        'calibration_date',
        'calibrated_by',
    )
    search_fields = (
        'equipment__name',
        'equipment__serial_number',
        'calibration_standard',
        'measurement_point',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    fieldsets = (
        ('Calibration Details', {
            'fields': (
                'equipment',
                'calibration_date',
                'calibrated_by',
                'calibration_standard',
                'measurement_point',
                'results',
            )
        }),
        ('Additional Information', {
            'fields': (
                'notes',
                'certificate_file',
            )
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = (
        'equipment',
        'maintenance_date',
        'performed_by',
        'service_provider',
        'returned_to_production',
    )
    list_filter = (
        'maintenance_date',
        'performed_by',
        'returned_to_production',
    )
    search_fields = (
        'equipment__name',
        'equipment__serial_number',
        'service_provider',
        'description',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    fieldsets = (
        ('Maintenance Details', {
            'fields': (
                'equipment',
                'maintenance_date',
                'performed_by',
                'service_provider',
                'description',
                'returned_to_production',
            )
        }),
        ('Additional Information', {
            'fields': (
                'notes',
                'certificate_file',
            )
        }),
        ('System Information', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
