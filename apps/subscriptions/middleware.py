from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _


class SubscriptionMiddleware:
    """Middleware to check subscription status and limits"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that don't require subscription check
        self.exempt_urls = [
            '/admin/',
            '/login/',
            '/logout/',
            '/register/',
            '/subscriptions/',
            '/static/',
            '/media/',
            '/i18n/',
        ]
    
    def __call__(self, request):
        # Check if URL is exempt
        path = request.path
        if any(path.startswith(url) for url in self.exempt_urls):
            return self.get_response(request)
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Check subscription status
        try:
            subscription = request.user.subscription
            
            # Check if subscription is expired or cancelled
            if subscription.status in ['expired', 'cancelled']:
                if not path.startswith('/subscriptions/'):
                    messages.warning(request, _('Your subscription has expired. Please renew to continue using the CRM.'))
                    return redirect('subscriptions:plans')
        except:
            # No subscription found, create free subscription
            from .models import Subscription
            Subscription.objects.create(
                user=request.user,
                plan='free',
                status='active'
            )
        
        return self.get_response(request)

