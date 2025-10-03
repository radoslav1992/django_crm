from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Subscription(models.Model):
    """User subscription model"""
    
    PLAN_CHOICES = [
        ('free', _('Free')),
        ('basic', _('Basic')),
        ('pro', _('Pro')),
        ('enterprise', _('Enterprise')),
    ]
    
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('cancelled', _('Cancelled')),
        ('expired', _('Expired')),
        ('past_due', _('Past Due')),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    
    plan = models.CharField(_('plan'), max_length=20, choices=PLAN_CHOICES, default='free')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Stripe subscription details
    stripe_subscription_id = models.CharField(_('Stripe subscription ID'), max_length=255, blank=True)
    stripe_customer_id = models.CharField(_('Stripe customer ID'), max_length=255, blank=True)
    stripe_price_id = models.CharField(_('Stripe price ID'), max_length=255, blank=True)
    
    # Subscription period
    current_period_start = models.DateTimeField(_('current period start'), null=True, blank=True)
    current_period_end = models.DateTimeField(_('current period end'), null=True, blank=True)
    
    # Billing
    cancel_at_period_end = models.BooleanField(_('cancel at period end'), default=False)
    
    # Usage tracking
    ai_requests_used = models.IntegerField(_('AI requests used this month'), default=0)
    ai_requests_reset_date = models.DateField(_('AI requests reset date'), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
    
    def __str__(self):
        return f"{self.user.email} - {self.get_plan_display()}"
    
    def get_plan_config(self):
        """Get plan configuration from settings"""
        return settings.SUBSCRIPTION_PLANS.get(self.plan, {})
    
    def can_use_feature(self, feature_name):
        """Check if user can use a specific feature"""
        plan_config = self.get_plan_config()
        features = plan_config.get('features', [])
        return feature_name in features
    
    def has_reached_contacts_limit(self):
        """Check if user has reached contacts limit"""
        plan_config = self.get_plan_config()
        limit = plan_config.get('contacts_limit', 0)
        
        if limit == -1:  # unlimited
            return False
        
        from apps.crm.models import Contact
        contact_count = Contact.objects.filter(owner=self.user).count()
        return contact_count >= limit
    
    def has_reached_users_limit(self):
        """Check if user has reached team members limit"""
        plan_config = self.get_plan_config()
        limit = plan_config.get('users_limit', 1)
        
        if limit == -1:  # unlimited
            return False
        
        from apps.accounts.models import TeamMember
        team_count = TeamMember.objects.filter(organization=self.user, is_active=True).count()
        return team_count >= limit
    
    def can_use_ai(self):
        """Check if user can use AI features"""
        plan_config = self.get_plan_config()
        monthly_limit = plan_config.get('ai_requests_per_month', 0)
        
        # Check if we need to reset the counter
        today = timezone.now().date()
        if not self.ai_requests_reset_date or self.ai_requests_reset_date < today:
            self.ai_requests_used = 0
            # Set reset date to first day of next month
            if today.month == 12:
                self.ai_requests_reset_date = today.replace(year=today.year + 1, month=1, day=1)
            else:
                self.ai_requests_reset_date = today.replace(month=today.month + 1, day=1)
            self.save()
        
        if monthly_limit == -1:  # unlimited
            return True
        
        return self.ai_requests_used < monthly_limit
    
    def increment_ai_usage(self):
        """Increment AI request counter"""
        self.ai_requests_used += 1
        self.save()
    
    def is_paid_plan(self):
        """Check if this is a paid plan"""
        return self.plan != 'free'


class SubscriptionHistory(models.Model):
    """History of subscription changes"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription_history')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='history')
    
    from_plan = models.CharField(_('from plan'), max_length=20)
    to_plan = models.CharField(_('to plan'), max_length=20)
    
    reason = models.TextField(_('reason'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('subscription history')
        verbose_name_plural = _('subscription histories')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email}: {self.from_plan} → {self.to_plan}"


class Invoice(models.Model):
    """Subscription invoice (Stripe)"""
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    
    stripe_invoice_id = models.CharField(_('Stripe invoice ID'), max_length=255, unique=True)
    
    amount_due = models.DecimalField(_('amount due'), max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(_('amount paid'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    
    status = models.CharField(_('status'), max_length=20)
    
    invoice_pdf = models.URLField(_('invoice PDF'), blank=True)
    hosted_invoice_url = models.URLField(_('hosted invoice URL'), blank=True)
    
    period_start = models.DateTimeField(_('period start'), null=True, blank=True)
    period_end = models.DateTimeField(_('period end'), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('subscription invoice')
        verbose_name_plural = _('subscription invoices')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invoice {self.stripe_invoice_id} - {self.amount_due} {self.currency}"

