from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import DocumentTemplate, TemplateVariable
from .forms import DocumentTemplateForm


@login_required
def template_list(request):
    """List all document templates"""
    templates = DocumentTemplate.objects.filter(owner=request.user)
    return render(request, 'templates/template_list.html', {'templates': templates})


@login_required
def template_create(request):
    """Create new document template"""
    if request.method == 'POST':
        form = DocumentTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            template.owner = request.user
            template.save()
            messages.success(request, _('Template created successfully.'))
            return redirect('templates:template_detail', pk=template.pk)
    else:
        form = DocumentTemplateForm()
    
    # Get available template variables
    variables = TemplateVariable.objects.all()
    
    return render(request, 'templates/template_form.html', {
        'form': form,
        'variables': variables,
        'action': 'create'
    })


@login_required
def template_detail(request, pk):
    """Template detail view"""
    template = get_object_or_404(DocumentTemplate, pk=pk, owner=request.user)
    variables = TemplateVariable.objects.filter(applies_to__in=[template.template_type, 'both'])
    
    return render(request, 'templates/template_detail.html', {
        'template': template,
        'variables': variables
    })


@login_required
def template_update(request, pk):
    """Update document template"""
    template = get_object_or_404(DocumentTemplate, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = DocumentTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, _('Template updated successfully.'))
            return redirect('templates:template_detail', pk=template.pk)
    else:
        form = DocumentTemplateForm(instance=template)
    
    # Get available template variables
    variables = TemplateVariable.objects.all()
    
    return render(request, 'templates/template_form.html', {
        'form': form,
        'template': template,
        'variables': variables,
        'action': 'update'
    })


@login_required
def template_delete(request, pk):
    """Delete template"""
    template = get_object_or_404(DocumentTemplate, pk=pk, owner=request.user)
    if request.method == 'POST':
        template.delete()
        messages.success(request, _('Template deleted successfully.'))
        return redirect('templates:template_list')
    
    return render(request, 'templates/template_confirm_delete.html', {'template': template})


@login_required
def template_preview(request, pk):
    """Preview template with sample data"""
    template = get_object_or_404(DocumentTemplate, pk=pk, owner=request.user)
    
    # Sample data for preview
    sample_data = {
        'invoice_number': 'INV-001',
        'invoice_date': '2025-10-03',
        'due_date': '2025-11-03',
        'client_name': 'Sample Client Ltd.',
        'client_address': '123 Main St, Sofia, Bulgaria',
        'items': [
            {'description': 'Web Development', 'quantity': 10, 'unit_price': 100, 'total': 1000},
            {'description': 'Design Services', 'quantity': 5, 'unit_price': 80, 'total': 400},
        ],
        'subtotal': 1400,
        'tax_amount': 280,
        'total': 1680,
    }
    
    return render(request, 'templates/template_preview.html', {
        'template': template,
        'sample_data': sample_data
    })


@login_required
def template_studio(request):
    """Template studio/editor interface"""
    templates = DocumentTemplate.objects.filter(owner=request.user)
    variables = TemplateVariable.objects.all()
    
    return render(request, 'templates/template_studio.html', {
        'templates': templates,
        'variables': variables
    })

