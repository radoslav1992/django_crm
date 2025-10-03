from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Company(models.Model):
    """Company/Organization model"""
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companies')
    
    name = models.CharField(_('company name'), max_length=200)
    website = models.URLField(_('website'), blank=True)
    industry = models.CharField(_('industry'), max_length=100, blank=True)
    employees = models.IntegerField(_('number of employees'), null=True, blank=True)
    annual_revenue = models.DecimalField(_('annual revenue'), max_digits=15, decimal_places=2, null=True, blank=True)
    
    phone = models.CharField(_('phone'), max_length=50, blank=True)
    email = models.EmailField(_('email'), blank=True)
    
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    
    vat_number = models.CharField(_('VAT number'), max_length=50, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    tags = models.CharField(_('tags'), max_length=500, blank=True, help_text=_('Comma-separated tags'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('crm:company_detail', kwargs={'pk': self.pk})


class Contact(models.Model):
    """Contact person model"""
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    position = models.CharField(_('position'), max_length=100, blank=True)
    
    email = models.EmailField(_('email'), blank=True)
    phone = models.CharField(_('phone'), max_length=50, blank=True)
    mobile = models.CharField(_('mobile'), max_length=50, blank=True)
    
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    tags = models.CharField(_('tags'), max_length=500, blank=True, help_text=_('Comma-separated tags'))
    
    # Social media
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    twitter = models.URLField(_('Twitter'), blank=True)
    facebook = models.URLField(_('Facebook'), blank=True)
    
    is_active = models.BooleanField(_('active'), default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('crm:contact_detail', kwargs={'pk': self.pk})
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Pipeline(models.Model):
    """Sales pipeline model"""
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pipelines')
    
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    is_default = models.BooleanField(_('default pipeline'), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('pipeline')
        verbose_name_plural = _('pipelines')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Stage(models.Model):
    """Deal stage in pipeline"""
    
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    
    name = models.CharField(_('name'), max_length=100)
    probability = models.IntegerField(_('win probability %'), default=0, help_text=_('0-100'))
    order = models.IntegerField(_('order'), default=0)
    
    class Meta:
        verbose_name = _('stage')
        verbose_name_plural = _('stages')
        ordering = ['pipeline', 'order']
    
    def __str__(self):
        return f"{self.pipeline.name} - {self.name}"


class Deal(models.Model):
    """Deal/Opportunity model"""
    
    STATUS_CHOICES = [
        ('open', _('Open')),
        ('won', _('Won')),
        ('lost', _('Lost')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deals')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals')
    
    name = models.CharField(_('deal name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    
    value = models.DecimalField(_('value'), max_digits=15, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    
    pipeline = models.ForeignKey(Pipeline, on_delete=models.SET_NULL, null=True, related_name='deals')
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, related_name='deals')
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='open')
    probability = models.IntegerField(_('probability %'), default=0)
    
    expected_close_date = models.DateField(_('expected close date'), null=True, blank=True)
    actual_close_date = models.DateField(_('actual close date'), null=True, blank=True)
    
    lost_reason = models.TextField(_('reason for loss'), blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    tags = models.CharField(_('tags'), max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('deal')
        verbose_name_plural = _('deals')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('crm:deal_detail', kwargs={'pk': self.pk})


class Task(models.Model):
    """Task model"""
    
    TYPE_CHOICES = [
        ('call', _('Call')),
        ('email', _('Email')),
        ('meeting', _('Meeting')),
        ('deadline', _('Deadline')),
        ('todo', _('To-Do')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    
    task_type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES, default='todo')
    priority = models.CharField(_('priority'), max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    due_date = models.DateTimeField(_('due date'), null=True, blank=True)
    completed = models.BooleanField(_('completed'), default=False)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        ordering = ['completed', '-due_date', '-created_at']
    
    def __str__(self):
        return self.title


class Activity(models.Model):
    """Activity log for CRM records"""
    
    TYPE_CHOICES = [
        ('note', _('Note')),
        ('call', _('Call')),
        ('email', _('Email')),
        ('meeting', _('Meeting')),
        ('task', _('Task')),
        ('deal_created', _('Deal Created')),
        ('deal_updated', _('Deal Updated')),
        ('deal_won', _('Deal Won')),
        ('deal_lost', _('Deal Lost')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    
    activity_type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.activity_type}: {self.title}"


class CustomField(models.Model):
    """Custom fields for CRM entities"""
    
    ENTITY_CHOICES = [
        ('contact', _('Contact')),
        ('company', _('Company')),
        ('deal', _('Deal')),
    ]
    
    FIELD_TYPE_CHOICES = [
        ('text', _('Text')),
        ('number', _('Number')),
        ('date', _('Date')),
        ('checkbox', _('Checkbox')),
        ('select', _('Select')),
        ('textarea', _('Text Area')),
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='custom_fields')
    
    entity_type = models.CharField(_('entity type'), max_length=20, choices=ENTITY_CHOICES)
    field_name = models.CharField(_('field name'), max_length=100)
    field_type = models.CharField(_('field type'), max_length=20, choices=FIELD_TYPE_CHOICES)
    field_options = models.JSONField(_('field options'), default=dict, blank=True)
    
    is_required = models.BooleanField(_('required'), default=False)
    order = models.IntegerField(_('order'), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('custom field')
        verbose_name_plural = _('custom fields')
        ordering = ['entity_type', 'order']
        unique_together = ['owner', 'entity_type', 'field_name']
    
    def __str__(self):
        return f"{self.entity_type}: {self.field_name}"

