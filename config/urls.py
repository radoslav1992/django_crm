"""
URL configuration for CRM project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from apps.accounts.health import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('crm/', include('apps.crm.urls')),
    path('invoices/', include('apps.invoices.urls')),
    path('templates/', include('apps.templates.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('ai/', include('apps.ai_assistant.urls')),
    path('faq/', include('apps.faq.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

