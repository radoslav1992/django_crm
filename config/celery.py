"""
Celery configuration for async tasks.
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('django_crm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'match-payments-daily': {
        'task': 'apps.invoices.tasks.match_payments_with_invoices',
        'schedule': crontab(hour=1, minute=0),  # Run daily at 1:00 AM
    },
    'send-payment-reminders': {
        'task': 'apps.invoices.tasks.send_payment_reminders',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9:00 AM
    },
}

