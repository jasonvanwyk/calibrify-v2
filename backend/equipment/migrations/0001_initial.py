# Generated by Django 4.2.7 on 2025-03-27 08:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(max_length=100)),
                ('purchase_date', models.DateField()),
                ('model_number', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('calibration_interval_type', models.CharField(choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], max_length=20)),
                ('calibration_interval_value', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_calibration_date', models.DateField(blank=True, null=True)),
                ('next_calibration_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_equipment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Equipment',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('service_provider', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('returned_to_production', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('certificate_file', models.FileField(blank=True, null=True, upload_to='maintenance_certificates/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_records', to='equipment.equipment')),
                ('performed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performed_maintenance', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Maintenance Records',
                'ordering': ['-maintenance_date'],
            },
        ),
        migrations.CreateModel(
            name='Calibration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calibration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('calibration_standard', models.CharField(max_length=200)),
                ('measurement_point', models.CharField(max_length=200)),
                ('results', models.TextField()),
                ('notes', models.TextField(blank=True)),
                ('certificate_file', models.FileField(blank=True, null=True, upload_to='calibration_certificates/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('calibrated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performed_calibrations', to=settings.AUTH_USER_MODEL)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calibrations', to='equipment.equipment')),
            ],
            options={
                'verbose_name_plural': 'Calibrations',
                'ordering': ['-calibration_date'],
            },
        ),
    ]
