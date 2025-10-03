from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('plans/', views.subscription_plans, name='plans'),
    path('checkout/<str:plan>/', views.create_checkout_session, name='checkout'),
    path('success/', views.subscription_success, name='success'),
    path('current/', views.current_subscription, name='current'),
    path('cancel/', views.cancel_subscription, name='cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]

