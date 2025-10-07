from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    # Invoices
    path('', views.invoice_list, name='invoice_list'),
    path('create/', views.invoice_create, name='invoice_create'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('<int:pk>/edit/', views.invoice_update, name='invoice_update'),
    path('<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
    path('<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('<int:pk>/send-email/', views.invoice_send_email, name='invoice_send_email'),
    
    # Offers
    path('offers/', views.offer_list, name='offer_list'),
    path('offers/create/', views.offer_create, name='offer_create'),
    path('offers/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('offers/<int:pk>/edit/', views.offer_update, name='offer_update'),
    path('offers/<int:pk>/delete/', views.offer_delete, name='offer_delete'),
    path('offers/<int:pk>/convert/', views.offer_convert_to_invoice, name='offer_convert'),
    path('offers/<int:pk>/send-email/', views.offer_send_email, name='offer_send_email'),
    
    # Payments
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
]

