from django import forms
from django.utils.translation import gettext_lazy as _
from .models import DocumentTemplate


class DocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = [
            'name', 'template_type', 'is_default',
            'header_content', 'footer_content',
            'primary_color', 'secondary_color', 'font_family',
            'logo', 'custom_css', 'html_template'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'template_type': forms.Select(attrs={'class': 'form-select'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'header_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'footer_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'font_family': forms.TextInput(attrs={'class': 'form-control'}),
            'custom_css': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Enter custom CSS...'}),
            'html_template': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'placeholder': 'Enter custom HTML template...'}),
        }

