from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from .models import AIConversation, AIMessage, AISuggestion
from .services import GeminiAssistant
from apps.crm.models import Contact, Deal
import json


@login_required
def ai_chat(request):
    """AI chat interface"""
    # Check if user can use AI
    subscription = request.user.subscription
    if not subscription.can_use_ai():
        messages.warning(request, _('You have reached your AI request limit for this month. Please upgrade your plan.'))
        return redirect('subscriptions:plans')
    
    # Get or create conversation
    conversation_id = request.GET.get('conversation')
    if conversation_id:
        conversation = get_object_or_404(AIConversation, id=conversation_id, user=request.user)
    else:
        conversation = AIConversation.objects.create(user=request.user, title=_('New conversation'))
    
    # Get all user conversations
    conversations = AIConversation.objects.filter(user=request.user)[:20]
    
    # Handle message submission
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        
        if user_message:
            # Create user message
            AIMessage.objects.create(
                conversation=conversation,
                role='user',
                content=user_message
            )
            
            # Get AI response
            assistant = GeminiAssistant(request.user)
            history = conversation.messages.all()[:10]  # Last 10 messages for context
            
            ai_response = assistant.chat(user_message, history)
            
            # Create assistant message
            AIMessage.objects.create(
                conversation=conversation,
                role='assistant',
                content=ai_response
            )
            
            # Update conversation title if it's the first message
            if conversation.messages.count() == 2:  # user + assistant
                conversation.title = user_message[:50]
                conversation.save()
            
            # Increment AI usage
            subscription.increment_ai_usage()
            
            return redirect(f'/ai/chat/?conversation={conversation.id}')
    
    return render(request, 'ai_assistant/chat.html', {
        'conversation': conversation,
        'conversations': conversations,
        'messages': conversation.messages.all(),
    })


@login_required
def ai_suggestions(request):
    """View AI suggestions"""
    suggestions = AISuggestion.objects.filter(user=request.user, is_dismissed=False)
    
    return render(request, 'ai_assistant/suggestions.html', {
        'suggestions': suggestions,
    })


@login_required
def generate_email(request, contact_id):
    """Generate email draft for contact"""
    subscription = request.user.subscription
    if not subscription.can_use_ai():
        return JsonResponse({'error': _('AI request limit reached')}, status=403)
    
    contact = get_object_or_404(Contact, id=contact_id, owner=request.user)
    
    if request.method == 'POST':
        purpose = request.POST.get('purpose', _('Follow-up'))
        
        assistant = GeminiAssistant(request.user)
        email_draft = assistant.generate_email_draft(contact, purpose)
        
        # Create suggestion
        AISuggestion.objects.create(
            user=request.user,
            suggestion_type='email',
            title=f'{_("Email draft for")} {contact.full_name}',
            content=email_draft,
            related_contact_id=contact.id
        )
        
        subscription.increment_ai_usage()
        
        return JsonResponse({'success': True, 'email': email_draft})
    
    return render(request, 'ai_assistant/generate_email.html', {'contact': contact})


@login_required
def analyze_deal_view(request, deal_id):
    """Analyze deal with AI"""
    subscription = request.user.subscription
    if not subscription.can_use_ai():
        messages.warning(request, _('You have reached your AI request limit for this month.'))
        return redirect('subscriptions:plans')
    
    deal = get_object_or_404(Deal, id=deal_id, owner=request.user)
    
    assistant = GeminiAssistant(request.user)
    analysis = assistant.analyze_deal(deal)
    
    # Create suggestion
    AISuggestion.objects.create(
        user=request.user,
        suggestion_type='deal',
        title=f'{_("Analysis for")} {deal.name}',
        content=analysis,
        related_deal_id=deal.id
    )
    
    subscription.increment_ai_usage()
    
    return render(request, 'ai_assistant/deal_analysis.html', {
        'deal': deal,
        'analysis': analysis,
    })


@login_required
def suggest_tasks_view(request):
    """Get AI task suggestions"""
    subscription = request.user.subscription
    if not subscription.can_use_ai():
        return JsonResponse({'error': _('AI request limit reached')}, status=403)
    
    assistant = GeminiAssistant(request.user)
    suggestions = assistant.suggest_tasks()
    
    subscription.increment_ai_usage()
    
    return JsonResponse({'success': True, 'suggestions': suggestions})


@login_required
def dismiss_suggestion(request, suggestion_id):
    """Dismiss an AI suggestion"""
    suggestion = get_object_or_404(AISuggestion, id=suggestion_id, user=request.user)
    suggestion.is_dismissed = True
    suggestion.save()
    
    messages.success(request, _('Suggestion dismissed.'))
    return redirect('ai_assistant:suggestions')


@login_required
def apply_suggestion(request, suggestion_id):
    """Mark suggestion as applied"""
    suggestion = get_object_or_404(AISuggestion, id=suggestion_id, user=request.user)
    suggestion.is_applied = True
    suggestion.save()
    
    messages.success(request, _('Suggestion applied.'))
    return redirect('ai_assistant:suggestions')


@login_required
def new_conversation(request):
    """Start a new AI conversation"""
    conversation = AIConversation.objects.create(
        user=request.user,
        title=_('New conversation')
    )
    return redirect(f'/ai/chat/?conversation={conversation.id}')


@login_required
def delete_conversation(request, conversation_id):
    """Delete an AI conversation"""
    conversation = get_object_or_404(AIConversation, id=conversation_id, user=request.user)
    
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, _('Conversation deleted.'))
        return redirect('ai_assistant:chat')
    
    return render(request, 'ai_assistant/conversation_confirm_delete.html', {
        'conversation': conversation
    })

