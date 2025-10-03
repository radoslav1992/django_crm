from django.contrib import admin
from .models import DocumentTemplate, TemplateVariable


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'is_default', 'owner', 'created_at')
    list_filter = ('template_type', 'is_default', 'created_at')
    search_fields = ('name',)
    ordering = ('-is_default', 'template_type', 'name')


@admin.register(TemplateVariable)
class TemplateVariableAdmin(admin.ModelAdmin):
    list_display = ('name', 'variable_type', 'applies_to', 'description')
    list_filter = ('variable_type', 'applies_to')
    search_fields = ('name', 'description')
    ordering = ('name',)

