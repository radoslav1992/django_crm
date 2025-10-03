from django.conf import settings


def subscription_context(request):
    """Add subscription info to template context"""
    context = {}
    
    if request.user.is_authenticated:
        try:
            subscription = request.user.subscription
            context['user_subscription'] = subscription
            context['user_plan'] = subscription.get_plan_config()
        except:
            context['user_subscription'] = None
            context['user_plan'] = settings.SUBSCRIPTION_PLANS.get('free', {})
    
    context['subscription_plans'] = settings.SUBSCRIPTION_PLANS
    
    return context

