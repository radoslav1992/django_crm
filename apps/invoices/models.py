from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from apps.crm.models import Contact, Company
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


class Invoice(models.Model):
    """Invoice model"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('paid', _('Paid')),
        ('partially_paid', _('Partially Paid')),
        ('overdue', _('Overdue')),
        ('cancelled', _('Cancelled')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    
    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True)
    invoice_date = models.DateField(_('invoice date'))
    due_date = models.DateField(_('due date'))
    
    # Client details (stored for record keeping)
    client_name = models.CharField(_('client name'), max_length=200)
    client_email = models.EmailField(_('client email'), blank=True)
    client_address = models.TextField(_('client address'), blank=True)
    client_vat_number = models.CharField(_('client VAT number'), max_length=50, blank=True)
    
    # Financial
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    subtotal = models.DecimalField(_('subtotal'), max_digits=15, decimal_places=2, default=0)
    tax_rate = models.DecimalField(_('tax rate %'), max_digits=5, decimal_places=2, default=20)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=15, decimal_places=2, default=0)
    paid_amount = models.DecimalField(_('paid amount'), max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Template reference
    template = models.ForeignKey('templates.DocumentTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment QR code
    qr_code = models.ImageField(_('QR code'), upload_to='invoices/qr_codes/', blank=True, null=True)
    payment_url = models.URLField(_('payment URL'), blank=True, help_text=_('Stripe payment link'))
    
    notes = models.TextField(_('notes'), blank=True)
    terms = models.TextField(_('terms and conditions'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        ordering = ['-invoice_date', '-invoice_number']
    
    def __str__(self):
        return f"{self.invoice_number} - {self.client_name}"
    
    def get_absolute_url(self):
        return reverse('invoices:invoice_detail', kwargs={'pk': self.pk})
    
    def calculate_totals(self):
        """Calculate invoice totals"""
        self.subtotal = sum(item.total for item in self.items.all())
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount
        self.save()
    
    def generate_qr_code(self):
        """Generate QR code for payment"""
        if self.payment_url:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.payment_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            filename = f'qr_code_{self.invoice_number}.png'
            self.qr_code.save(filename, File(buffer), save=False)
            self.save()
    
    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount
    
    @property
    def is_paid(self):
        return self.paid_amount >= self.total_amount


class InvoiceItem(models.Model):
    """Invoice line item"""
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    
    description = models.CharField(_('description'), max_length=500)
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(_('unit price'), max_digits=15, decimal_places=2)
    total = models.DecimalField(_('total'), max_digits=15, decimal_places=2)
    
    order = models.IntegerField(_('order'), default=0)
    
    class Meta:
        verbose_name = _('invoice item')
        verbose_name_plural = _('invoice items')
        ordering = ['invoice', 'order']
    
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Update invoice totals
        self.invoice.calculate_totals()
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"


class Offer(models.Model):
    """Offer/Quote model"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('expired', _('Expired')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='offers')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='offers')
    
    offer_number = models.CharField(_('offer number'), max_length=50, unique=True)
    offer_date = models.DateField(_('offer date'))
    valid_until = models.DateField(_('valid until'))
    
    # Client details
    client_name = models.CharField(_('client name'), max_length=200)
    client_email = models.EmailField(_('client email'), blank=True)
    client_address = models.TextField(_('client address'), blank=True)
    
    # Financial
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    subtotal = models.DecimalField(_('subtotal'), max_digits=15, decimal_places=2, default=0)
    tax_rate = models.DecimalField(_('tax rate %'), max_digits=5, decimal_places=2, default=20)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Template reference
    template = models.ForeignKey('templates.DocumentTemplate', on_delete=models.SET_NULL, null=True, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    terms = models.TextField(_('terms and conditions'), blank=True)
    
    # Conversion to invoice
    converted_to_invoice = models.OneToOneField(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='converted_from_offer'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('offer')
        verbose_name_plural = _('offers')
        ordering = ['-offer_date', '-offer_number']
    
    def __str__(self):
        return f"{self.offer_number} - {self.client_name}"
    
    def get_absolute_url(self):
        return reverse('invoices:offer_detail', kwargs={'pk': self.pk})
    
    def calculate_totals(self):
        """Calculate offer totals"""
        self.subtotal = sum(item.total for item in self.items.all())
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount
        self.save()


class OfferItem(models.Model):
    """Offer line item"""
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='items')
    
    description = models.CharField(_('description'), max_length=500)
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(_('unit price'), max_digits=15, decimal_places=2)
    total = models.DecimalField(_('total'), max_digits=15, decimal_places=2)
    
    order = models.IntegerField(_('order'), default=0)
    
    class Meta:
        verbose_name = _('offer item')
        verbose_name_plural = _('offer items')
        ordering = ['offer', 'order']
    
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Update offer totals
        self.offer.calculate_totals()
    
    def __str__(self):
        return f"{self.offer.offer_number} - {self.description}"


class Payment(models.Model):
    """Payment record"""
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', _('Stripe')),
        ('bank_transfer', _('Bank Transfer')),
        ('cash', _('Cash')),
        ('check', _('Check')),
        ('other', _('Other')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    
    payment_date = models.DateField(_('payment date'))
    amount = models.DecimalField(_('amount'), max_digits=15, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    # Stripe payment details
    stripe_payment_intent_id = models.CharField(_('Stripe Payment Intent ID'), max_length=255, blank=True)
    stripe_charge_id = models.CharField(_('Stripe Charge ID'), max_length=255, blank=True)
    
    reference = models.CharField(_('reference'), max_length=200, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    is_matched = models.BooleanField(_('matched to invoice'), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')
        ordering = ['-payment_date', '-created_at']
    
    def __str__(self):
        return f"Payment {self.amount} {self.currency} - {self.payment_date}"
    
    def match_to_invoice(self):
        """Try to automatically match payment to invoice"""
        if self.invoice or self.is_matched:
            return
        
        # Try to find matching invoice by amount and currency
        potential_invoices = Invoice.objects.filter(
            owner=self.owner,
            currency=self.currency,
            status__in=['sent', 'partially_paid', 'overdue']
        )
        
        # Look for exact amount match
        for invoice in potential_invoices:
            if invoice.balance_due == self.amount:
                self.invoice = invoice
                self.is_matched = True
                self.save()
                
                # Update invoice
                invoice.paid_amount += self.amount
                if invoice.is_paid:
                    invoice.status = 'paid'
                else:
                    invoice.status = 'partially_paid'
                invoice.save()
                break

