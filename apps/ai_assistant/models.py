from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AIConversation(models.Model):
    """AI conversation thread"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_conversations')
    
    title = models.CharField(_('title'), max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('AI conversation')
        verbose_name_plural = _('AI conversations')
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title or f"Conversation {self.id}"


class AIMessage(models.Model):
    """Individual message in AI conversation"""
    
    ROLE_CHOICES = [
        ('user', _('User')),
        ('assistant', _('Assistant')),
    ]
    
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES)
    content = models.TextField(_('content'))
    
    # Context information
    context_data = models.JSONField(_('context data'), default=dict, blank=True, help_text=_('CRM data context for the message'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('AI message')
        verbose_name_plural = _('AI messages')
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class AISuggestion(models.Model):
    """AI-generated suggestions for CRM actions"""
    
    SUGGESTION_TYPE_CHOICES = [
        ('email', _('Email Draft')),
        ('task', _('Task Suggestion')),
        ('deal', _('Deal Insight')),
        ('contact', _('Contact Recommendation')),
        ('template', _('Template Content')),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_suggestions')
    
    suggestion_type = models.CharField(_('type'), max_length=20, choices=SUGGESTION_TYPE_CHOICES)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'))
    
    # Related objects
    related_contact_id = models.IntegerField(_('related contact ID'), null=True, blank=True)
    related_company_id = models.IntegerField(_('related company ID'), null=True, blank=True)
    related_deal_id = models.IntegerField(_('related deal ID'), null=True, blank=True)
    
    is_applied = models.BooleanField(_('applied'), default=False)
    is_dismissed = models.BooleanField(_('dismissed'), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('AI suggestion')
        verbose_name_plural = _('AI suggestions')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_suggestion_type_display()}: {self.title}"

