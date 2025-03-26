# ============================================================================
# File Path: backend/equipment/models.py
# Description: Models for equipment management system
# ============================================================================

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Equipment(models.Model):
    """Model for tracking equipment items."""
    
    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    purchase_date = models.DateField()
    model_number = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    calibration_interval_type = models.CharField(
        max_length=20,
        choices=[
            ('days', 'Days'),
            ('weeks', 'Weeks'),
            ('months', 'Months'),
            ('years', 'Years'),
        ]
    )
    calibration_interval_value = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_equipment'
    )
    last_calibration_date = models.DateField(null=True, blank=True)
    next_calibration_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.created_by = kwargs.pop('user', None)
        super().save(*args, **kwargs)

class Calibration(models.Model):
    """Model for tracking equipment calibrations."""
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='calibrations'
    )
    calibration_date = models.DateTimeField(default=timezone.now)
    calibrated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='performed_calibrations'
    )
    calibration_standard = models.CharField(max_length=200)
    measurement_point = models.CharField(max_length=200)
    results = models.TextField()
    notes = models.TextField(blank=True)
    certificate_file = models.FileField(
        upload_to='calibration_certificates/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-calibration_date']
        verbose_name_plural = 'Calibrations'

    def __str__(self):
        return f"Calibration of {self.equipment.name} on {self.calibration_date}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.calibrated_by = kwargs.pop('user', None)
            # Update equipment's last and next calibration dates
            self.equipment.last_calibration_date = self.calibration_date.date()
            # Calculate next calibration date based on interval
            interval_days = self.equipment.calibration_interval_value
            if self.equipment.calibration_interval_type == 'days':
                interval_days *= 1
            elif self.equipment.calibration_interval_type == 'weeks':
                interval_days *= 7
            elif self.equipment.calibration_interval_type == 'months':
                interval_days *= 30
            elif self.equipment.calibration_interval_type == 'years':
                interval_days *= 365
            self.equipment.next_calibration_date = (
                self.calibration_date.date() + timezone.timedelta(days=interval_days)
            )
            self.equipment.save()
        super().save(*args, **kwargs)

class Maintenance(models.Model):
    """Model for tracking equipment maintenance."""
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )
    maintenance_date = models.DateTimeField(default=timezone.now)
    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='performed_maintenance'
    )
    service_provider = models.CharField(max_length=200)
    description = models.TextField()
    returned_to_production = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    certificate_file = models.FileField(
        upload_to='maintenance_certificates/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-maintenance_date']
        verbose_name_plural = 'Maintenance Records'

    def __str__(self):
        return f"Maintenance of {self.equipment.name} on {self.maintenance_date}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.performed_by = kwargs.pop('user', None)
        super().save(*args, **kwargs)
