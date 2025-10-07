from django.urls import path
from . import views

app_name = 'templates'

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('create/', views.template_create, name='template_create'),
    path('<int:pk>/', views.template_detail, name='template_detail'),
    path('<int:pk>/edit/', views.template_update, name='template_update'),
    path('<int:pk>/delete/', views.template_delete, name='template_delete'),
    path('<int:pk>/preview/', views.template_preview, name='template_preview'),
    path('studio/', views.template_studio, name='template_studio'),
    # AI-powered template generation
    path('ai/generate/', views.generate_ai_template, name='generate_ai_template'),
    path('ai/refine/', views.refine_ai_template, name='refine_ai_template'),
    path('ai/save/', views.save_ai_template, name='save_ai_template'),
]

