from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import DocumentTemplate, TemplateVariable, EmailTemplate
from .forms import DocumentTemplateForm
from apps.ai_assistant.services import GeminiAssistant
import json


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
    """AI-powered template studio/editor interface"""
    templates = DocumentTemplate.objects.filter(owner=request.user)
    email_templates = EmailTemplate.objects.filter(owner=request.user)
    variables = TemplateVariable.objects.all()
    
    return render(request, 'templates/template_studio.html', {
        'templates': templates,
        'email_templates': email_templates,
        'variables': variables
    })


@login_required
@require_POST
def generate_ai_template(request):
    """Generate template using AI based on user prompt"""
    import logging
    from django.core.cache import cache
    
    logger = logging.getLogger(__name__)
    
    try:
        # Check AI usage limit
        subscription = request.user.subscription
        if not subscription.can_use_ai():
            return JsonResponse({
                'success': False,
                'error': _('You have reached your AI request limit for this month. Please upgrade your plan.'),
                'upgrade_required': True
            }, status=403)
        
        # Rate limiting - max 5 requests per minute
        rate_limit_key = f"ai_template_gen:{request.user.id}"
        requests_count = cache.get(rate_limit_key, 0)
        if requests_count >= 5:
            return JsonResponse({
                'success': False,
                'error': _('Too many requests. Please wait a moment and try again.')
            }, status=429)
        cache.set(rate_limit_key, requests_count + 1, 60)  # 60 seconds
        
        # Parse and validate request
        data = json.loads(request.body)
        user_prompt = data.get('prompt', '').strip()
        template_type = data.get('template_type', 'invoice')
        
        # Input validation
        MAX_PROMPT_LENGTH = 2000
        if not user_prompt:
            return JsonResponse({
                'success': False,
                'error': _('Please provide a description for your template')
            }, status=400)
        
        if len(user_prompt) > MAX_PROMPT_LENGTH:
            return JsonResponse({
                'success': False,
                'error': _('Description is too long. Please keep it under 2000 characters.')
            }, status=400)
        
        # Initialize AI assistant
        assistant = GeminiAssistant(request.user)
        
        # Generate template with timeout protection
        html_content = assistant.generate_complete_template(user_prompt, template_type)
        
        # Validate output size
        MAX_HTML_SIZE = 100000  # 100KB
        if len(html_content) > MAX_HTML_SIZE:
            logger.warning(f"Generated template too large for user {request.user.id}: {len(html_content)} bytes")
            return JsonResponse({
                'success': False,
                'error': _('Generated template is too large. Please simplify your requirements.')
            }, status=400)
        
        # Increment AI usage counter
        subscription.increment_ai_usage()
        
        return JsonResponse({
            'success': True,
            'html_content': html_content,
            'message': _('Template generated successfully!'),
            'ai_requests_remaining': subscription.get_plan_config().get('ai_requests_per_month', 0) - subscription.ai_requests_used
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': _('Invalid request format')
        }, status=400)
    
    except Exception as e:
        logger.error(f"AI template generation failed for user {request.user.id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': _('Failed to generate template. Please try again.')
        }, status=500)


@login_required
@require_POST
def refine_ai_template(request):
    """Refine existing template based on user feedback"""
    import logging
    from django.core.cache import cache
    
    logger = logging.getLogger(__name__)
    
    try:
        # Check AI usage limit
        subscription = request.user.subscription
        if not subscription.can_use_ai():
            return JsonResponse({
                'success': False,
                'error': _('You have reached your AI request limit for this month. Please upgrade your plan.'),
                'upgrade_required': True
            }, status=403)
        
        # Rate limiting - max 5 requests per minute
        rate_limit_key = f"ai_template_refine:{request.user.id}"
        requests_count = cache.get(rate_limit_key, 0)
        if requests_count >= 5:
            return JsonResponse({
                'success': False,
                'error': _('Too many requests. Please wait a moment and try again.')
            }, status=429)
        cache.set(rate_limit_key, requests_count + 1, 60)
        
        # Parse and validate request
        data = json.loads(request.body)
        current_html = data.get('current_html', '')
        user_feedback = data.get('feedback', '').strip()
        
        # Input validation
        MAX_FEEDBACK_LENGTH = 1000
        MAX_HTML_SIZE = 100000
        
        if not current_html or not user_feedback:
            return JsonResponse({
                'success': False,
                'error': _('Please provide both current template and feedback')
            }, status=400)
        
        if len(user_feedback) > MAX_FEEDBACK_LENGTH:
            return JsonResponse({
                'success': False,
                'error': _('Feedback is too long. Please keep it under 1000 characters.')
            }, status=400)
        
        if len(current_html) > MAX_HTML_SIZE:
            return JsonResponse({
                'success': False,
                'error': _('Current template is too large.')
            }, status=400)
        
        # Initialize AI assistant
        assistant = GeminiAssistant(request.user)
        
        # Refine template
        refined_html = assistant.refine_template(current_html, user_feedback)
        
        # Validate output size
        if len(refined_html) > MAX_HTML_SIZE:
            logger.warning(f"Refined template too large for user {request.user.id}: {len(refined_html)} bytes")
            return JsonResponse({
                'success': False,
                'error': _('Refined template is too large. Please simplify your requirements.')
            }, status=400)
        
        # Increment AI usage counter
        subscription.increment_ai_usage()
        
        return JsonResponse({
            'success': True,
            'html_content': refined_html,
            'message': _('Template refined successfully!'),
            'ai_requests_remaining': subscription.get_plan_config().get('ai_requests_per_month', 0) - subscription.ai_requests_used
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': _('Invalid request format')
        }, status=400)
    
    except Exception as e:
        logger.error(f"AI template refinement failed for user {request.user.id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': _('Failed to refine template. Please try again.')
        }, status=500)


@login_required
@require_POST
def save_ai_template(request):
    """Save AI-generated template to database"""
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Parse and validate request
        data = json.loads(request.body)
        template_name = data.get('name', '').strip()
        template_type = data.get('template_type', 'invoice')
        html_content = data.get('html_content', '')
        is_default = data.get('is_default', False)
        
        # Input validation
        MAX_NAME_LENGTH = 200
        MAX_HTML_SIZE = 100000
        
        if not template_name or not html_content:
            return JsonResponse({
                'success': False,
                'error': _('Please provide template name and content')
            }, status=400)
        
        if len(template_name) > MAX_NAME_LENGTH:
            return JsonResponse({
                'success': False,
                'error': _('Template name is too long. Please keep it under 200 characters.')
            }, status=400)
        
        if len(html_content) > MAX_HTML_SIZE:
            return JsonResponse({
                'success': False,
                'error': _('Template content is too large.')
            }, status=400)
        
        # Validate template type
        if template_type not in ['invoice', 'offer']:
            return JsonResponse({
                'success': False,
                'error': _('Invalid template type')
            }, status=400)
        
        # Sanitize HTML content - allow only safe tags for templates
        allowed_tags = [
            'html', 'head', 'body', 'title', 'meta', 'link', 'style',
            'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'table', 'thead', 'tbody', 'tr', 'td', 'th',
            'ul', 'ol', 'li', 'br', 'hr', 'img',
            'strong', 'em', 'b', 'i', 'u', 'small',
            'header', 'footer', 'section', 'article'
        ]
        
        allowed_attributes = {
            '*': ['class', 'id', 'style'],
            'img': ['src', 'alt', 'width', 'height'],
            'link': ['href', 'rel'],
            'meta': ['charset', 'name', 'content']
        }
        
        # Note: bleach.clean will strip Django template tags, so we need to preserve them
        # For now, we'll just validate size and store as-is
        # In production, consider using a Django template validator
        
        # Create template
        template = DocumentTemplate.objects.create(
            owner=request.user,
            name=template_name,
            template_type=template_type,
            html_template=html_content,
            is_default=is_default
        )
        
        logger.info(f"User {request.user.id} saved AI-generated template: {template.pk}")
        
        return JsonResponse({
            'success': True,
            'template_id': template.pk,
            'message': _('Template saved successfully!'),
            'redirect_url': f'/templates/{template.pk}/'
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': _('Invalid request format')
        }, status=400)
    
    except Exception as e:
        logger.error(f"Failed to save template for user {request.user.id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': _('Failed to save template. Please try again.')
        }, status=500)


@login_required
@require_POST
def generate_ai_email_template(request):
    """Generate email template using AI based on user prompt"""
    import logging
    from django.core.cache import cache
    
    logger = logging.getLogger(__name__)
    
    try:
        # Check AI usage limit
        subscription = request.user.subscription
        if not subscription.can_use_ai():
            return JsonResponse({
                'success': False,
                'error': _('You have reached your AI request limit for this month. Please upgrade your plan.'),
                'upgrade_required': True
            }, status=403)
        
        # Rate limiting
        rate_limit_key = f"ai_email_template_gen:{request.user.id}"
        requests_count = cache.get(rate_limit_key, 0)
        if requests_count >= 5:
            return JsonResponse({
                'success': False,
                'error': _('Too many requests. Please wait a moment and try again.')
            }, status=429)
        cache.set(rate_limit_key, requests_count + 1, 60)
        
        # Parse request
        data = json.loads(request.body)
        user_prompt = data.get('prompt', '').strip()
        template_type = data.get('template_type', 'custom')
        
        if not user_prompt:
            return JsonResponse({
                'success': False,
                'error': _('Please provide a description for your email template')
            }, status=400)
        
        if len(user_prompt) > 2000:
            return JsonResponse({
                'success': False,
                'error': _('Description is too long. Please keep it under 2000 characters.')
            }, status=400)
        
        # Initialize AI assistant
        assistant = GeminiAssistant(request.user)
        
        # Generate email template
        result = assistant.generate_email_template(user_prompt, template_type)
        
        # Increment AI usage
        subscription.increment_ai_usage()
        
        return JsonResponse({
            'success': True,
            'subject': result['subject'],
            'html_content': result['html_content'],
            'plain_text': result.get('plain_text', ''),
            'message': _('Email template generated successfully!'),
            'ai_requests_remaining': subscription.get_plan_config().get('ai_requests_per_month', 0) - subscription.ai_requests_used
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': _('Invalid request format')
        }, status=400)
    
    except Exception as e:
        logger.error(f"AI email template generation failed for user {request.user.id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': _('Failed to generate email template. Please try again.')
        }, status=500)


@login_required
@require_POST
def save_ai_email_template(request):
    """Save AI-generated email template to database"""
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Parse request
        data = json.loads(request.body)
        template_name = data.get('name', '').strip()
        template_type = data.get('template_type', 'custom')
        subject = data.get('subject', '').strip()
        html_content = data.get('html_content', '')
        plain_text = data.get('plain_text', '')
        is_default = data.get('is_default', False)
        ai_prompt = data.get('ai_prompt', '')
        
        # Validation
        if not template_name or not subject or not html_content:
            return JsonResponse({
                'success': False,
                'error': _('Please provide template name, subject, and content')
            }, status=400)
        
        if len(template_name) > 200:
            return JsonResponse({
                'success': False,
                'error': _('Template name is too long')
            }, status=400)
        
        if len(subject) > 500:
            return JsonResponse({
                'success': False,
                'error': _('Subject is too long')
            }, status=400)
        
        if len(html_content) > 100000:
            return JsonResponse({
                'success': False,
                'error': _('Template content is too large')
            }, status=400)
        
        # Check if name already exists
        if EmailTemplate.objects.filter(owner=request.user, name=template_name).exists():
            return JsonResponse({
                'success': False,
                'error': _('A template with this name already exists')
            }, status=400)
        
        # Create email template
        template = EmailTemplate.objects.create(
            owner=request.user,
            name=template_name,
            template_type=template_type,
            subject=subject,
            html_content=html_content,
            plain_text=plain_text,
            is_default=is_default,
            ai_generated=True,
            ai_prompt=ai_prompt
        )
        
        logger.info(f"User {request.user.id} saved AI-generated email template: {template.pk}")
        
        return JsonResponse({
            'success': True,
            'template_id': template.pk,
            'message': _('Email template saved successfully!')
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': _('Invalid request format')
        }, status=400)
    
    except Exception as e:
        logger.error(f"Failed to save email template for user {request.user.id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': _('Failed to save email template. Please try again.')
        }, status=500)


@login_required
def email_template_list(request):
    """List all email templates"""
    templates = EmailTemplate.objects.filter(owner=request.user)
    return render(request, 'templates/email_template_list.html', {'email_templates': templates})


@login_required
def email_template_detail(request, pk):
    """Email template detail view"""
    template = get_object_or_404(EmailTemplate, pk=pk, owner=request.user)
    return render(request, 'templates/email_template_detail.html', {'template': template})


@login_required
def email_template_delete(request, pk):
    """Delete email template"""
    template = get_object_or_404(EmailTemplate, pk=pk, owner=request.user)
    if request.method == 'POST':
        template.delete()
        messages.success(request, _('Email template deleted successfully.'))
        return redirect('templates:email_template_list')
    
    return render(request, 'templates/email_template_confirm_delete.html', {'template': template})

