from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class DocumentTemplate(models.Model):
    """Template for invoices and offers"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('invoice', _('Invoice')),
        ('offer', _('Offer')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='document_templates')
    
    name = models.CharField(_('template name'), max_length=200)
    template_type = models.CharField(_('template type'), max_length=20, choices=TEMPLATE_TYPE_CHOICES)
    
    is_default = models.BooleanField(_('default template'), default=False)
    
    # Template content (JSON structure for flexibility)
    header_content = models.TextField(_('header content'), blank=True)
    footer_content = models.TextField(_('footer content'), blank=True)
    
    # Styling
    primary_color = models.CharField(_('primary color'), max_length=7, default='#007bff')
    secondary_color = models.CharField(_('secondary color'), max_length=7, default='#6c757d')
    font_family = models.CharField(_('font family'), max_length=100, default='Arial, sans-serif')
    
    # Logo
    logo = models.ImageField(_('logo'), upload_to='templates/logos/', blank=True, null=True)
    
    # Layout settings (JSON)
    layout_settings = models.JSONField(_('layout settings'), default=dict, blank=True)
    
    # Custom CSS
    custom_css = models.TextField(_('custom CSS'), blank=True)
    
    # Custom HTML template
    html_template = models.TextField(_('HTML template'), blank=True, help_text=_('Custom HTML template with placeholders'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('document template')
        verbose_name_plural = _('document templates')
        ordering = ['-is_default', 'template_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def save(self, *args, **kwargs):
        # Ensure only one default per type per user
        if self.is_default:
            DocumentTemplate.objects.filter(
                owner=self.owner,
                template_type=self.template_type,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        
        super().save(*args, **kwargs)


class TemplateVariable(models.Model):
    """Available variables for templates"""
    
    VARIABLE_TYPE_CHOICES = [
        ('text', _('Text')),
        ('number', _('Number')),
        ('date', _('Date')),
        ('currency', _('Currency')),
        ('image', _('Image')),
    ]
    
    name = models.CharField(_('variable name'), max_length=100, unique=True)
    description = models.CharField(_('description'), max_length=500)
    variable_type = models.CharField(_('variable type'), max_length=20, choices=VARIABLE_TYPE_CHOICES)
    example_value = models.CharField(_('example value'), max_length=200)
    
    applies_to = models.CharField(_('applies to'), max_length=50, help_text=_('invoice, offer, or both'))
    
    class Meta:
        verbose_name = _('template variable')
        verbose_name_plural = _('template variables')
        ordering = ['name']
    
    def __str__(self):
        return f"{{{{{self.name}}}}} - {self.description}"


class EmailTemplate(models.Model):
    """Custom email templates for sending invoices, offers, and custom emails"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('invoice', _('Invoice Email')),
        ('offer', _('Offer Email')),
        ('custom', _('Custom Email')),
        ('reminder', _('Payment Reminder')),
        ('welcome', _('Welcome Email')),
        ('follow_up', _('Follow-up Email')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_templates')
    
    name = models.CharField(_('template name'), max_length=200)
    template_type = models.CharField(_('template type'), max_length=20, choices=TEMPLATE_TYPE_CHOICES)
    
    subject = models.CharField(_('email subject'), max_length=500, help_text=_('Can include template variables like {{contact_name}}'))
    
    # Email body
    html_content = models.TextField(_('HTML content'), help_text=_('HTML email body with template variables'))
    plain_text = models.TextField(_('plain text version'), blank=True, help_text=_('Plain text fallback (auto-generated if empty)'))
    
    # Settings
    is_default = models.BooleanField(_('default template'), default=False, help_text=_('Use this as the default for this type'))
    is_active = models.BooleanField(_('active'), default=True)
    
    # AI-generated metadata
    ai_generated = models.BooleanField(_('AI generated'), default=False)
    ai_prompt = models.TextField(_('AI prompt'), blank=True, help_text=_('Original prompt used to generate this template'))
    
    # Usage tracking
    times_sent = models.IntegerField(_('times sent'), default=0)
    last_used_at = models.DateTimeField(_('last used at'), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('email template')
        verbose_name_plural = _('email templates')
        ordering = ['-is_default', 'template_type', 'name']
        unique_together = [['owner', 'name']]
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def save(self, *args, **kwargs):
        # Ensure only one default per type per user
        if self.is_default:
            EmailTemplate.objects.filter(
                owner=self.owner,
                template_type=self.template_type,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        
        super().save(*args, **kwargs)
    
    def increment_usage(self):
        """Increment usage counter and update last used timestamp"""
        from django.utils import timezone
        self.times_sent += 1
        self.last_used_at = timezone.now()
        self.save(update_fields=['times_sent', 'last_used_at'])
    
    def render(self, context):
        """
        Render the template with the given context
        
        Args:
            context: Dictionary of variables to use in template
        
        Returns:
            Tuple of (subject, html_content, plain_text)
        """
        from django.template import Template, Context
        
        # Render subject
        subject_template = Template(self.subject)
        rendered_subject = subject_template.render(Context(context))
        
        # Render HTML content
        html_template = Template(self.html_content)
        rendered_html = html_template.render(Context(context))
        
        # Render or generate plain text
        if self.plain_text:
            text_template = Template(self.plain_text)
            rendered_text = text_template.render(Context(context))
        else:
            # Simple HTML to text conversion
            from html import unescape
            import re
            rendered_text = re.sub(r'<[^>]+>', '', rendered_html)
            rendered_text = unescape(rendered_text)
            rendered_text = re.sub(r'\n\s*\n', '\n\n', rendered_text)
        
        return rendered_subject, rendered_html, rendered_text

