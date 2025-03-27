# ============================================================================
# File Path: frontend/views.py
# Description: View functions for Calibrify frontend
# ============================================================================

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from equipment.models import Equipment, Calibration, Maintenance
from django.db.models import Q


@login_required
def dashboard(request):
    """
    Dashboard view showing equipment statistics, upcoming events,
    and recent activities. Requires user authentication.
    """
    # Get current date for comparisons
    today = timezone.now().date()
    thirty_days_ahead = today + timedelta(days=30)
    start_of_month = today.replace(day=1)

    # Equipment statistics
    total_equipment = Equipment.objects.count()
    
    # Due calibrations (calibration_date within next 30 days)
    due_calibrations = Calibration.objects.filter(
        Q(calibration_date__gte=today) & 
        Q(calibration_date__lte=thirty_days_ahead) &
        ~Q(results='Completed')  # Not completed calibrations
    ).count()

    # Overdue maintenance (based on maintenance_date)
    overdue_maintenance = Maintenance.objects.filter(
        Q(maintenance_date__lt=today) & 
        ~Q(returned_to_production=True)  # Not returned to production
    ).count()

    # Completed this month
    completed_this_month = (
        Calibration.objects.filter(
            updated_at__gte=start_of_month,
            results='Completed'
        ).count() +
        Maintenance.objects.filter(
            updated_at__gte=start_of_month,
            returned_to_production=True
        ).count()
    )

    # Upcoming events (combine calibrations and maintenance)
    upcoming_calibrations = Calibration.objects.filter(
        calibration_date__gte=today,
        calibration_date__lte=thirty_days_ahead,
    ).order_by('calibration_date')[:5]

    upcoming_maintenance = Maintenance.objects.filter(
        maintenance_date__gte=today,
        maintenance_date__lte=thirty_days_ahead
    ).order_by('maintenance_date')[:5]

    # Combine and sort upcoming events
    upcoming_events = []
    for cal in upcoming_calibrations:
        upcoming_events.append({
            'date': cal.calibration_date,
            'title': f'Calibration: {cal.equipment.name}',
            'equipment': cal.equipment,
            'type': 'Calibration',
            'status': 'Pending' if not cal.results else cal.results
        })

    for maint in upcoming_maintenance:
        upcoming_events.append({
            'date': maint.maintenance_date,
            'title': f'Maintenance: {maint.equipment.name}',
            'equipment': maint.equipment,
            'type': 'Maintenance',
            'status': 'Completed' if maint.returned_to_production else 'Pending'
        })

    # Sort combined events by date
    upcoming_events.sort(key=lambda x: x['date'])
    upcoming_events = upcoming_events[:5]  # Limit to 5 most recent

    # Recent activities (combine recent calibrations and maintenance)
    recent_calibrations = Calibration.objects.filter(
        updated_at__gte=start_of_month
    ).order_by('-updated_at')[:5]

    recent_maintenance = Maintenance.objects.filter(
        updated_at__gte=start_of_month
    ).order_by('-updated_at')[:5]

    # Combine and format recent activities
    recent_activities = []
    for cal in recent_calibrations:
        status = 'pending' if not cal.results else cal.results.lower()
        recent_activities.append({
            'icon': 'ri-calendar-check-line',
            'description': f'Calibration {status} for {cal.equipment.name}',
            'timestamp': cal.updated_at
        })

    for maint in recent_maintenance:
        status = 'completed' if maint.returned_to_production else 'pending'
        recent_activities.append({
            'icon': 'ri-tools-line',
            'description': (f'Maintenance {status} for '
                          f'{maint.equipment.name}'),
            'timestamp': maint.updated_at
        })

    # Sort activities by timestamp
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activities = recent_activities[:5]  # Limit to 5 most recent

    context = {
        'total_equipment': total_equipment,
        'due_calibrations': due_calibrations,
        'overdue_maintenance': overdue_maintenance,
        'completed_this_month': completed_this_month,
        'upcoming_events': upcoming_events,
        'recent_activities': recent_activities,
    }

    return render(request, 'dashboard.html', context)

@login_required
def equipment_list(request):
    """
    Display list of all equipment with filtering and sorting options.
    """
    equipment = Equipment.objects.all().order_by('name')
    return render(request, 'equipment/list.html', {'equipment': equipment})

@login_required
def equipment_detail(request, pk):
    """
    Display detailed information about a specific piece of equipment.
    """
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'equipment/detail.html', {'equipment': equipment})

@login_required
def equipment_edit(request, pk):
    """
    Edit an existing piece of equipment.
    """
    equipment = get_object_or_404(Equipment, pk=pk)
    return render(request, 'equipment/edit.html', {'equipment': equipment})

@login_required
def equipment_create(request):
    """
    Create new equipment entry.
    """
    return render(request, 'equipment/create.html')

@login_required
def calibration_list(request):
    """
    Display list of all calibrations with filtering and sorting options.
    """
    calibrations = Calibration.objects.all().order_by('-calibration_date')
    return render(request, 'calibration/list.html', {'calibrations': calibrations})

@login_required
def calibration_create(request):
    """
    Create new calibration entry.
    """
    return render(request, 'calibration/create.html')

@login_required
def maintenance_list(request):
    """
    Display list of all maintenance records with filtering and sorting options.
    """
    maintenance = Maintenance.objects.all().order_by('-maintenance_date')
    return render(request, 'maintenance/list.html', {'maintenance': maintenance})

@login_required
def maintenance_create(request):
    """
    Create new maintenance record.
    """
    return render(request, 'maintenance/create.html')

@login_required
def reports(request):
    """
    Display reports and analytics dashboard.
    """
    return render(request, 'reports/index.html')

@login_required
def calendar(request):
    """
    Display calendar view of all events.
    """
    return render(request, 'calendar/index.html') 