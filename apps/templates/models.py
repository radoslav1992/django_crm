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

