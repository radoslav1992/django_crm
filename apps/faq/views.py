from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from django.db import models
from .models import FAQCategory, FAQItem
import markdown
import os
from django.conf import settings


def faq_home(request):
    """FAQ home page with all categories"""
    categories = FAQCategory.objects.filter(is_active=True).prefetch_related('items')
    featured_items = FAQItem.objects.filter(is_active=True, is_featured=True)[:6]
    
    # Get current language
    lang = get_language()
    
    # Prepare language-aware data
    categories_data = []
    for cat in categories:
        categories_data.append({
            'obj': cat,
            'name': cat.name_en if (lang == 'en' and cat.name_en) else cat.name,
            'description': cat.description
        })
    
    featured_data = []
    for item in featured_items:
        featured_data.append({
            'obj': item,
            'question': item.question_en if (lang == 'en' and item.question_en) else item.question,
            'category_name': item.category.name_en if (lang == 'en' and item.category.name_en) else item.category.name
        })
    
    return render(request, 'faq/faq_home.html', {
        'categories': categories_data,
        'featured_items': featured_data,
        'current_lang': lang
    })


def faq_category(request, slug):
    """FAQ category view with all questions"""
    category = get_object_or_404(FAQCategory, slug=slug, is_active=True)
    items = category.items.filter(is_active=True)
    
    # Get current language
    lang = get_language()
    
    # Prepare language-aware data
    category_name = category.name_en if (lang == 'en' and category.name_en) else category.name
    category_desc = category.description
    
    items_data = []
    for item in items:
        items_data.append({
            'obj': item,
            'question': item.question_en if (lang == 'en' and item.question_en) else item.question,
            'answer': item.answer_en if (lang == 'en' and item.answer_en) else item.answer
        })
    
    return render(request, 'faq/faq_category.html', {
        'category': category,
        'category_name': category_name,
        'category_desc': category_desc,
        'items': items_data,
        'current_lang': lang
    })


def faq_detail(request, pk):
    """FAQ question detail view"""
    item = get_object_or_404(FAQItem, pk=pk, is_active=True)
    
    # Increment view counter
    item.increment_views()
    
    # Get current language
    lang = get_language()
    
    # Choose appropriate content based on language
    if lang == 'en' and item.question_en:
        question = item.question_en
        answer = item.answer_en if item.answer_en else item.answer
    else:
        question = item.question
        answer = item.answer
    
    # Convert markdown to HTML
    answer_html = markdown.markdown(
        answer,
        extensions=['extra', 'codehilite', 'fenced_code', 'tables']
    )
    
    # Load guide file if specified
    guide_html = None
    if item.guide_file:
        guide_path = os.path.join(
            settings.BASE_DIR, 
            'apps', 'faq', 'guides', 
            item.guide_file
        )
        if os.path.exists(guide_path):
            with open(guide_path, 'r', encoding='utf-8') as f:
                guide_content = f.read()
                guide_html = markdown.markdown(
                    guide_content,
                    extensions=['extra', 'codehilite', 'fenced_code', 'tables']
                )
    
    # Get related questions from same category
    related_items = FAQItem.objects.filter(
        category=item.category,
        is_active=True
    ).exclude(pk=item.pk)[:5]
    
    return render(request, 'faq/faq_detail.html', {
        'item': item,
        'question': question,
        'answer_html': answer_html,
        'guide_html': guide_html,
        'related_items': related_items
    })


def faq_search(request):
    """Search FAQ"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        lang = get_language()
        if lang == 'en':
            results = FAQItem.objects.filter(
                is_active=True
            ).filter(
                models.Q(question_en__icontains=query) |
                models.Q(answer_en__icontains=query) |
                models.Q(question__icontains=query) |
                models.Q(answer__icontains=query)
            )
        else:
            results = FAQItem.objects.filter(
                is_active=True
            ).filter(
                models.Q(question__icontains=query) |
                models.Q(answer__icontains=query)
            )
    
    return render(request, 'faq/faq_search.html', {
        'query': query,
        'results': results
    })

