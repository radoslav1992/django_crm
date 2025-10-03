from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Invoice, Payment


@shared_task
def match_payments_with_invoices():
    """Automatically match unmatched payments with invoices"""
    unmatched_payments = Payment.objects.filter(is_matched=False, invoice__isnull=True)
    
    matched_count = 0
    for payment in unmatched_payments:
        payment.match_to_invoice()
        if payment.is_matched:
            matched_count += 1
    
    return f"Matched {matched_count} payments"


@shared_task
def send_payment_reminders():
    """Send payment reminders for overdue invoices"""
    today = timezone.now().date()
    
    # Mark overdue invoices
    overdue_invoices = Invoice.objects.filter(
        status__in=['sent', 'partially_paid'],
        due_date__lt=today
    )
    
    for invoice in overdue_invoices:
        invoice.status = 'overdue'
        invoice.save()
    
    return f"Updated {overdue_invoices.count()} overdue invoices"


@shared_task
def generate_invoice_qr_codes():
    """Generate QR codes for invoices that have payment URLs but no QR code"""
    invoices_without_qr = Invoice.objects.filter(
        payment_url__isnull=False
    ).exclude(payment_url='').filter(qr_code='')
    
    count = 0
    for invoice in invoices_without_qr:
        invoice.generate_qr_code()
        count += 1
    
    return f"Generated {count} QR codes"

