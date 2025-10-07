"""Health check endpoint for load balancers and monitoring"""
from django.http import JsonResponse
from django.db import connection
import redis
from django.conf import settings


def health_check(request):
    """
    Health check endpoint that verifies critical services are running.
    Returns 200 if healthy, 503 if any service is down.
    """
    health = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health['checks']['database'] = 'ok'
    except Exception as e:
        health['status'] = 'unhealthy'
        health['checks']['database'] = f'error: {str(e)}'
    
    # Check Redis connectivity
    try:
        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        health['checks']['redis'] = 'ok'
    except Exception as e:
        health['status'] = 'unhealthy'
        health['checks']['redis'] = f'error: {str(e)}'
    
    # Check if critical settings are configured
    if not settings.SECRET_KEY or settings.SECRET_KEY == 'django-insecure-change-this-in-production':
        health['status'] = 'unhealthy'
        health['checks']['secret_key'] = 'not_configured'
    else:
        health['checks']['secret_key'] = 'ok'
    
    status_code = 200 if health['status'] == 'healthy' else 503
    return JsonResponse(health, status=status_code)

