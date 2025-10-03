from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def subscription_plans(request):
    """Display subscription plans"""
    plans = settings.SUBSCRIPTION_PLANS
    
    try:
        current_subscription = request.user.subscription
    except:
        from .models import Subscription
        current_subscription = Subscription.objects.create(
            user=request.user,
            plan='free',
            status='active'
        )
    
    return render(request, 'subscriptions/plans.html', {
        'plans': plans,
        'current_subscription': current_subscription,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })


@login_required
def create_checkout_session(request, plan):
    """Create Stripe checkout session"""
    if plan not in settings.SUBSCRIPTION_PLANS:
        messages.error(request, _('Invalid plan selected.'))
        return redirect('subscriptions:plans')
    
    if plan == 'free':
        # Update to free plan
        subscription = request.user.subscription
        old_plan = subscription.plan
        subscription.plan = 'free'
        subscription.status = 'active'
        subscription.save()
        
        from .models import SubscriptionHistory
        SubscriptionHistory.objects.create(
            user=request.user,
            subscription=subscription,
            from_plan=old_plan,
            to_plan='free'
        )
        
        messages.success(request, _('Subscription updated to Free plan.'))
        return redirect('subscriptions:current')
    
    try:
        # Get or create Stripe customer
        subscription = request.user.subscription
        
        if not subscription.stripe_customer_id:
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.get_full_name() or request.user.username,
                metadata={'user_id': request.user.id}
            )
            subscription.stripe_customer_id = customer.id
            subscription.save()
        
        # Get price ID for the plan
        price_id_map = {
            'basic': settings.STRIPE_PRICE_BASIC,
            'pro': settings.STRIPE_PRICE_PRO,
            'enterprise': settings.STRIPE_PRICE_ENTERPRISE,
        }
        
        price_id = price_id_map.get(plan)
        if not price_id:
            messages.error(request, _('Plan configuration error.'))
            return redirect('subscriptions:plans')
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            customer=subscription.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/subscriptions/success/'),
            cancel_url=request.build_absolute_uri('/subscriptions/plans/'),
            metadata={
                'user_id': request.user.id,
                'plan': plan,
            }
        )
        
        return redirect(checkout_session.url)
    
    except Exception as e:
        messages.error(request, f'{_("Error creating checkout session")}: {str(e)}')
        return redirect('subscriptions:plans')


@login_required
def subscription_success(request):
    """Subscription success page"""
    messages.success(request, _('Subscription activated successfully! Welcome to your new plan.'))
    return redirect('subscriptions:current')


@login_required
def current_subscription(request):
    """Display current subscription details"""
    try:
        subscription = request.user.subscription
    except:
        from .models import Subscription
        subscription = Subscription.objects.create(
            user=request.user,
            plan='free',
            status='active'
        )
    
    plan_config = subscription.get_plan_config()
    
    # Get subscription history
    from .models import SubscriptionHistory
    history = SubscriptionHistory.objects.filter(user=request.user)[:10]
    
    # Get invoices
    invoices = subscription.invoices.all()[:10] if hasattr(subscription, 'invoices') else []
    
    return render(request, 'subscriptions/current.html', {
        'subscription': subscription,
        'plan_config': plan_config,
        'history': history,
        'invoices': invoices,
    })


@login_required
def cancel_subscription(request):
    """Cancel subscription"""
    if request.method == 'POST':
        subscription = request.user.subscription
        
        if subscription.stripe_subscription_id:
            try:
                # Cancel at period end
                stripe.Subscription.modify(
                    subscription.stripe_subscription_id,
                    cancel_at_period_end=True
                )
                
                subscription.cancel_at_period_end = True
                subscription.save()
                
                messages.info(request, _('Your subscription will be cancelled at the end of the current billing period.'))
            except Exception as e:
                messages.error(request, f'{_("Error cancelling subscription")}: {str(e)}')
        else:
            # Free plan, just update status
            old_plan = subscription.plan
            subscription.plan = 'free'
            subscription.status = 'active'
            subscription.save()
            
            from .models import SubscriptionHistory
            SubscriptionHistory.objects.create(
                user=request.user,
                subscription=subscription,
                from_plan=old_plan,
                to_plan='free',
                reason='User cancelled subscription'
            )
            
            messages.success(request, _('Subscription cancelled successfully.'))
        
        return redirect('subscriptions:current')
    
    return render(request, 'subscriptions/cancel_confirm.html')


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session_completed(session)
    
    elif event['type'] == 'invoice.paid':
        invoice = event['data']['object']
        handle_invoice_paid(invoice)
    
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        handle_invoice_payment_failed(invoice)
    
    elif event['type'] == 'customer.subscription.updated':
        subscription_data = event['data']['object']
        handle_subscription_updated(subscription_data)
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription_data = event['data']['object']
        handle_subscription_deleted(subscription_data)
    
    return HttpResponse(status=200)


def handle_checkout_session_completed(session):
    """Handle successful checkout"""
    from apps.accounts.models import User
    from .models import Subscription, SubscriptionHistory
    
    user_id = session['metadata'].get('user_id')
    plan = session['metadata'].get('plan')
    
    if user_id and plan:
        user = User.objects.get(id=user_id)
        subscription = user.subscription
        
        old_plan = subscription.plan
        subscription.plan = plan
        subscription.status = 'active'
        subscription.stripe_subscription_id = session.get('subscription')
        subscription.save()
        
        # Create history entry
        SubscriptionHistory.objects.create(
            user=user,
            subscription=subscription,
            from_plan=old_plan,
            to_plan=plan
        )


def handle_invoice_paid(invoice_data):
    """Handle paid invoice"""
    from .models import Subscription, Invoice as SubInvoice
    
    subscription_id = invoice_data.get('subscription')
    if subscription_id:
        try:
            subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
            
            # Create or update invoice record
            SubInvoice.objects.update_or_create(
                stripe_invoice_id=invoice_data['id'],
                defaults={
                    'subscription': subscription,
                    'amount_due': invoice_data['amount_due'] / 100,
                    'amount_paid': invoice_data['amount_paid'] / 100,
                    'currency': invoice_data['currency'].upper(),
                    'status': invoice_data['status'],
                    'invoice_pdf': invoice_data.get('invoice_pdf', ''),
                    'hosted_invoice_url': invoice_data.get('hosted_invoice_url', ''),
                }
            )
        except Subscription.DoesNotExist:
            pass


def handle_invoice_payment_failed(invoice_data):
    """Handle failed payment"""
    from .models import Subscription
    
    subscription_id = invoice_data.get('subscription')
    if subscription_id:
        try:
            subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)
            subscription.status = 'past_due'
            subscription.save()
        except Subscription.DoesNotExist:
            pass


def handle_subscription_updated(subscription_data):
    """Handle subscription update"""
    from .models import Subscription
    from django.utils import timezone
    
    try:
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_data['id'])
        subscription.status = subscription_data['status']
        subscription.current_period_start = timezone.datetime.fromtimestamp(subscription_data['current_period_start'])
        subscription.current_period_end = timezone.datetime.fromtimestamp(subscription_data['current_period_end'])
        subscription.cancel_at_period_end = subscription_data.get('cancel_at_period_end', False)
        subscription.save()
    except Subscription.DoesNotExist:
        pass


def handle_subscription_deleted(subscription_data):
    """Handle subscription deletion"""
    from .models import Subscription, SubscriptionHistory
    
    try:
        subscription = Subscription.objects.get(stripe_subscription_id=subscription_data['id'])
        old_plan = subscription.plan
        subscription.plan = 'free'
        subscription.status = 'cancelled'
        subscription.save()
        
        # Create history entry
        SubscriptionHistory.objects.create(
            user=subscription.user,
            subscription=subscription,
            from_plan=old_plan,
            to_plan='free',
            reason='Subscription ended'
        )
    except Subscription.DoesNotExist:
        pass

