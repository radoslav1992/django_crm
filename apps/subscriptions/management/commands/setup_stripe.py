"""
Django management command to automatically set up Stripe products and prices.
This creates all subscription plans and updates the .env file automatically.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import stripe
import os
import re


class Command(BaseCommand):
    help = 'Automatically creates Stripe products and prices, then updates .env file'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔧 Stripe Products Setup\n'))
        self.stdout.write('=' * 50)
        
        # Initialize Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        if not stripe.api_key or stripe.api_key == 'your_stripe_secret_key':
            self.stdout.write(self.style.ERROR(
                '\n❌ Error: STRIPE_SECRET_KEY not configured in .env file'
            ))
            self.stdout.write('Please add your Stripe secret key to .env file first.')
            return
        
        self.stdout.write(f'\n✅ Connected to Stripe')
        self.stdout.write(f'   Using key: {stripe.api_key[:12]}...\n')
        
        # Define products
        products_config = [
            {
                'name': 'Free Plan',
                'description': 'Free CRM features - 50 contacts, 10 companies, 5 deals/month',
                'price': 0,  # €0.00
                'env_key': 'STRIPE_PRICE_FREE'
            },
            {
                'name': 'Basic Plan',
                'description': 'Essential CRM with AI - 500 contacts, 100 companies, 50 deals/month',
                'price': 999,  # €9.99
                'env_key': 'STRIPE_PRICE_BASIC'
            },
            {
                'name': 'Pro Plan',
                'description': 'Advanced CRM - 5,000 contacts, 1,000 companies, unlimited deals',
                'price': 2999,  # €29.99
                'env_key': 'STRIPE_PRICE_PRO'
            },
            {
                'name': 'Enterprise Plan',
                'description': 'Full-featured CRM - Unlimited everything with dedicated support',
                'price': 9999,  # €99.99
                'env_key': 'STRIPE_PRICE_ENTERPRISE'
            }
        ]
        
        price_ids = {}
        
        # Create each product and price
        for idx, config in enumerate(products_config, 1):
            self.stdout.write(f'\n{idx}️⃣  Creating {config["name"]}...')
            
            try:
                # Create product
                product = stripe.Product.create(
                    name=config['name'],
                    description=config['description']
                )
                
                self.stdout.write(f'   ✅ Product created: {product.id}')
                
                # Create price
                price = stripe.Price.create(
                    product=product.id,
                    unit_amount=config['price'],
                    currency='eur',
                    recurring={'interval': 'month'}
                )
                
                price_display = f"€{config['price']/100:.2f}/month"
                self.stdout.write(f'   ✅ Price created: {price.id} ({price_display})')
                
                price_ids[config['env_key']] = price.id
                
            except stripe.error.StripeError as e:
                self.stdout.write(self.style.ERROR(f'   ❌ Error: {str(e)}'))
                return
        
        # Update .env file
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('\n✅ All products created successfully!\n'))
        self.stdout.write('\n📝 Updating .env file...')
        
        env_path = os.path.join(settings.BASE_DIR, '.env')
        
        if not os.path.exists(env_path):
            self.stdout.write(self.style.ERROR('   ❌ .env file not found'))
            return
        
        # Read current .env
        with open(env_path, 'r') as f:
            env_content = f.read()
        
        # Update each price ID
        for env_key, price_id in price_ids.items():
            pattern = rf'{env_key}=.*'
            replacement = f'{env_key}={price_id}'
            env_content = re.sub(pattern, replacement, env_content)
        
        # Write updated .env
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        self.stdout.write('   ✅ .env file updated\n')
        
        # Display summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('\n🎉 Setup Complete!\n'))
        self.stdout.write('\n📋 Your new price IDs:\n')
        
        for env_key, price_id in price_ids.items():
            self.stdout.write(f'   {env_key}={price_id}')
        
        self.stdout.write('\n\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('\n✨ Next Steps:\n'))
        self.stdout.write('\n1. ✅ Restart your Django server to load new .env values')
        self.stdout.write('2. ✅ Visit: http://localhost:8001/bg/subscriptions/plans/')
        self.stdout.write('3. ✅ Test subscriptions with card: 4242 4242 4242 4242')
        self.stdout.write('\n\n🚀 Your Stripe subscriptions are ready!\n')
