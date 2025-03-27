# ============================================================================
# File Path: backend/calibrify/health/views.py
# Description: Health check views for Docker container monitoring
# ============================================================================

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache

def health_check(request):
    """
    Basic health check that verifies:
    1. The application is running
    2. Database connection is working
    3. Cache connection is working
    """
    # Check database connection
    db_healthy = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_healthy = False

    # Check cache connection
    cache_healthy = True
    try:
        cache.set('health_check', 'ok', 1)
        cache_value = cache.get('health_check')
        if cache_value != 'ok':
            cache_healthy = False
    except Exception:
        cache_healthy = False

    status = 200 if (db_healthy and cache_healthy) else 503
    health_status = {
        'status': 'healthy' if status == 200 else 'unhealthy',
        'database': 'up' if db_healthy else 'down',
        'cache': 'up' if cache_healthy else 'down',
    }

    return JsonResponse(health_status, status=status) 