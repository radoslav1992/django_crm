from django.contrib import admin
from .models import Invoice, InvoiceItem, Offer, OfferItem, Payment


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client_name', 'invoice_date', 'due_date', 'total_amount', 'paid_amount', 'status', 'owner')
    list_filter = ('status', 'invoice_date', 'due_date')
    search_fields = ('invoice_number', 'client_name', 'client_email')
    ordering = ('-invoice_date', '-invoice_number')
    inlines = [InvoiceItemInline]


class OfferItemInline(admin.TabularInline):
    model = OfferItem
    extra = 1


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('offer_number', 'client_name', 'offer_date', 'valid_until', 'total_amount', 'status', 'owner')
    list_filter = ('status', 'offer_date', 'valid_until')
    search_fields = ('offer_number', 'client_name', 'client_email')
    ordering = ('-offer_date', '-offer_number')
    inlines = [OfferItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'amount', 'currency', 'payment_method', 'invoice', 'is_matched', 'owner')
    list_filter = ('payment_method', 'is_matched', 'payment_date')
    search_fields = ('reference', 'stripe_payment_intent_id', 'stripe_charge_id')
    ordering = ('-payment_date', '-created_at')

