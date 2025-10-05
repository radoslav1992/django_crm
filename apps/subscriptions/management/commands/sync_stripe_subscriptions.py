"""
Django management command to sync subscriptions from Stripe.
This fixes subscriptions that weren't updated due to missing webhooks.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from apps.accounts.models import User
from apps.subscriptions.models import Subscription, SubscriptionHistory
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = 'Sync subscriptions from Stripe to fix missing updates'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔄 Syncing Subscriptions from Stripe\n'))
        self.stdout.write('=' * 50)
        
        # Get all users with Stripe customer IDs
        users_with_stripe = Subscription.objects.exclude(stripe_customer_id__isnull=True).exclude(stripe_customer_id='')
        
        self.stdout.write(f'\nFound {users_with_stripe.count()} users with Stripe customers\n')
        
        updated_count = 0
        
        for subscription in users_with_stripe:
            user = subscription.user
            self.stdout.write(f'\n📋 Checking {user.email}...')
            self.stdout.write(f'   Current plan: {subscription.plan}')
            self.stdout.write(f'   Stripe customer: {subscription.stripe_customer_id}')
            
            try:
                # Get all subscriptions for this customer from Stripe
                stripe_subscriptions = stripe.Subscription.list(
                    customer=subscription.stripe_customer_id,
                    status='active',
                    limit=10
                )
                
                if stripe_subscriptions.data:
                    # Get the most recent active subscription
                    stripe_sub = stripe_subscriptions.data[0]
                    
                    self.stdout.write(f'   ✅ Found active Stripe subscription: {stripe_sub.id}')
                    
                    # Get the price ID
                    price_id = stripe_sub['items']['data'][0]['price']['id']
                    self.stdout.write(f'   Price ID: {price_id}')
                    
                    # Map price ID to plan
                    plan_map = {
                        settings.STRIPE_PRICE_FREE: 'free',
                        settings.STRIPE_PRICE_BASIC: 'basic',
                        settings.STRIPE_PRICE_PRO: 'pro',
                        settings.STRIPE_PRICE_ENTERPRISE: 'enterprise',
                    }
                    
                    new_plan = plan_map.get(price_id)
                    
                    if new_plan and new_plan != subscription.plan:
                        old_plan = subscription.plan
                        subscription.plan = new_plan
                        subscription.status = 'active'
                        subscription.stripe_subscription_id = stripe_sub.id
                        subscription.save()
                        
                        # Create history entry
                        SubscriptionHistory.objects.create(
                            user=user,
                            subscription=subscription,
                            from_plan=old_plan,
                            to_plan=new_plan,
                            reason='Synced from Stripe'
                        )
                        
                        self.stdout.write(self.style.SUCCESS(
                            f'   🎉 Updated {user.email}: {old_plan} → {new_plan}'
                        ))
                        updated_count += 1
                    elif new_plan == subscription.plan:
                        self.stdout.write(f'   ℹ️  Already up to date ({new_plan})')
                    else:
                        self.stdout.write(f'   ⚠️  Unknown price ID: {price_id}')
                else:
                    self.stdout.write(f'   ℹ️  No active subscriptions in Stripe')
            
            except stripe.error.StripeError as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Stripe error: {str(e)}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Error: {str(e)}'))
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Sync complete! Updated {updated_count} subscription(s)\n'))
