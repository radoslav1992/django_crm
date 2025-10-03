from django.contrib import admin
from .models import Subscription, SubscriptionHistory, Invoice


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'current_period_end', 'ai_requests_used', 'created_at')
    list_filter = ('plan', 'status', 'created_at')
    search_fields = ('user__email', 'stripe_subscription_id', 'stripe_customer_id')
    ordering = ('-created_at',)


@admin.register(SubscriptionHistory)
class SubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_plan', 'to_plan', 'created_at')
    list_filter = ('from_plan', 'to_plan', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('stripe_invoice_id', 'subscription', 'amount_due', 'amount_paid', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('stripe_invoice_id', 'subscription__user__email')
    ordering = ('-created_at',)

