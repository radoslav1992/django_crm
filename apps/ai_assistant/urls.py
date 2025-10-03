from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('chat/', views.ai_chat, name='chat'),
    path('chat/new/', views.new_conversation, name='new_conversation'),
    path('chat/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    
    path('suggestions/', views.ai_suggestions, name='suggestions'),
    path('suggestions/<int:suggestion_id>/dismiss/', views.dismiss_suggestion, name='dismiss_suggestion'),
    path('suggestions/<int:suggestion_id>/apply/', views.apply_suggestion, name='apply_suggestion'),
    
    path('generate-email/<int:contact_id>/', views.generate_email, name='generate_email'),
    path('analyze-deal/<int:deal_id>/', views.analyze_deal_view, name='analyze_deal'),
    path('suggest-tasks/', views.suggest_tasks_view, name='suggest_tasks'),
]

