from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.faq_home, name='home'),
    path('search/', views.faq_search, name='search'),
    path('category/<slug:slug>/', views.faq_category, name='category'),
    path('question/<int:pk>/', views.faq_detail, name='detail'),
]

