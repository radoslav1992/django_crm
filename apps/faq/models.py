from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class FAQCategory(models.Model):
    """FAQ Categories"""
    
    name = models.CharField(_('име'), max_length=200)
    name_en = models.CharField(_('име (английски)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('описание'), blank=True)
    icon = models.CharField(_('икона'), max_length=50, default='bi-question-circle', 
                           help_text=_('Bootstrap icon класс (напр. bi-envelope)'))
    order = models.IntegerField(_('ред'), default=0)
    is_active = models.BooleanField(_('активен'), default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('faq:category', kwargs={'slug': self.slug})


class FAQItem(models.Model):
    """FAQ Questions and Answers"""
    
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, 
                                 related_name='items', verbose_name=_('категория'))
    
    question = models.CharField(_('въпрос'), max_length=500)
    question_en = models.CharField(_('въпрос (английски)'), max_length=500, blank=True)
    
    # Answer can be stored as markdown
    answer = models.TextField(_('отговор'), help_text=_('Markdown формат'))
    answer_en = models.TextField(_('отговор (английски)'), blank=True, help_text=_('Markdown формат'))
    
    # Optional: Link to detailed guide file
    guide_file = models.CharField(_('файл с ръководство'), max_length=200, blank=True,
                                  help_text=_('Име на MD файл в faq/guides/ (напр. stripe-setup.md)'))
    
    order = models.IntegerField(_('ред'), default=0)
    is_active = models.BooleanField(_('активен'), default=True)
    views_count = models.IntegerField(_('брой прегледи'), default=0)
    is_featured = models.BooleanField(_('препоръчан'), default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('въпрос')
        verbose_name_plural = _('въпроси')
        ordering = ['category', 'order', 'question']
    
    def __str__(self):
        return self.question
    
    def increment_views(self):
        """Increment view counter"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def get_absolute_url(self):
        return reverse('faq:detail', kwargs={'pk': self.pk})

