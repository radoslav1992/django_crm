from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with additional fields"""
    
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    company_name = models.CharField(_('company name'), max_length=200, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    
    # Stripe keys for user's customers (not platform subscription)
    stripe_publishable_key = models.CharField(
        _('Stripe publishable key'),
        max_length=255,
        blank=True,
        help_text=_('User\'s Stripe publishable key for accepting payments from their customers')
    )
    stripe_secret_key = models.CharField(
        _('Stripe secret key'),
        max_length=255,
        blank=True,
        help_text=_('User\'s Stripe secret key for accepting payments from their customers')
    )
    
    # Resend email configuration
    resend_api_key = models.CharField(
        _('Resend API key'),
        max_length=255,
        blank=True,
        help_text=_('Your Resend API key for sending emails')
    )
    resend_from_email = models.EmailField(
        _('From email address'),
        blank=True,
        help_text=_('Email address to send emails from (must be verified in Resend)')
    )
    resend_from_name = models.CharField(
        _('From name'),
        max_length=200,
        blank=True,
        help_text=_('Name to display in "from" field of emails')
    )
    
    # Organization info
    vat_number = models.CharField(_('VAT number'), max_length=50, blank=True)
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    
    # Preferences
    language = models.CharField(
        _('language'),
        max_length=5,
        choices=[('bg', 'Български'), ('en', 'English')],
        default='bg'
    )
    timezone = models.CharField(_('timezone'), max_length=50, default='Europe/Sofia')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email
    
    def has_stripe_configured(self):
        """Check if user has configured their Stripe keys"""
        return bool(self.stripe_publishable_key and self.stripe_secret_key)
    
    def has_resend_configured(self):
        """Check if user has configured Resend"""
        return bool(self.resend_api_key and self.resend_from_email)


class TeamMember(models.Model):
    """Team members for multi-user accounts"""
    
    ROLE_CHOICES = [
        ('owner', _('Owner')),
        ('admin', _('Admin')),
        ('manager', _('Manager')),
        ('user', _('User')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    organization = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    permissions = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('team member')
        verbose_name_plural = _('team members')
        unique_together = ['user', 'organization']
    
    def __str__(self):
        return f"{self.user.email} - {self.organization.company_name}"

