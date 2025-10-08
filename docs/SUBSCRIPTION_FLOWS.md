# 💳 Subscription & Payment Flows Documentation

Complete guide to how subscriptions, payments, upgrades, and failures are handled in the Django CRM.

---

## 1️⃣ What happens when a user makes a subscription and pays?

### **Complete Flow:**

```
User → Subscribe Button → Stripe Checkout → Payment → Success → Updated Subscription
```

### **Step-by-Step Process:**

#### **Step 1: User Initiates Subscription**
- User visits: `/bg/subscriptions/plans/`
- Clicks "Избери [Plan Name]" button (e.g., "Избери Basic")

#### **Step 2: Create Stripe Checkout Session**
```python
# In apps/subscriptions/views.py - create_checkout_session()

# Get or create Stripe customer
if not subscription.stripe_customer_id:
    customer = stripe.Customer.create(
        email=request.user.email,
        name=request.user.get_full_name(),
        metadata={'user_id': request.user.id}
    )
    subscription.stripe_customer_id = customer.id

# Create checkout session
checkout_session = stripe.checkout.Session.create(
    customer=subscription.stripe_customer_id,
    payment_method_types=['card'],
    line_items=[{
        'price': price_id,  # e.g., price_1SEsPTBaLmgw9EfzzjJN9LwQ
        'quantity': 1,
    }],
    mode='subscription',
    success_url='/subscriptions/success/?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='/subscriptions/plans/',
    metadata={
        'user_id': str(request.user.id),
        'plan': 'basic',  # or pro/enterprise
    }
)
```

#### **Step 3: Stripe Checkout Page**
- User redirected to Stripe's secure payment page
- Enters card details (Test: 4242 4242 4242 4242)
- Stripe validates and processes payment
- Creates subscription in Stripe

#### **Step 4: Payment Successful**
- Stripe charges the card
- Creates subscription record in Stripe
- Generates invoice
- Redirects back to success URL with `session_id`

#### **Step 5: Success Handler**
```python
# In apps/subscriptions/views.py - subscription_success()

# Retrieve session from Stripe
session = stripe.checkout.Session.retrieve(session_id)

# Extract metadata
user_id = session['metadata'].get('user_id')
plan = session['metadata'].get('plan')  # 'basic', 'pro', or 'enterprise'

# Update subscription in database
subscription = request.user.subscription
old_plan = subscription.plan

subscription.plan = plan
subscription.status = 'active'
subscription.stripe_subscription_id = session.get('subscription')
subscription.save()

# Create history record
SubscriptionHistory.objects.create(
    user=request.user,
    subscription=subscription,
    from_plan=old_plan,
    to_plan=plan
)
```

#### **Step 6: User Confirmation**
- Redirected to `/bg/subscriptions/current/`
- Sees success message: "Subscription upgraded to Basic plan successfully!"
- Features immediately unlocked

### **What Gets Stored:**

```python
# Subscription Model
subscription.plan = 'basic'  # Plan name
subscription.status = 'active'  # Subscription status
subscription.stripe_customer_id = 'cus_TBEop8CjG32Yk3'  # Stripe customer
subscription.stripe_subscription_id = 'sub_1SEsRNBaLmgw9EfzuFLSm9OQ'  # Stripe sub
subscription.current_period_start = datetime(...)  # Billing period start
subscription.current_period_end = datetime(...)  # Billing period end

# History Record
history.from_plan = 'free'
history.to_plan = 'basic'
history.created_at = now()
```

### **Webhook Events (if configured):**

1. **`checkout.session.completed`**
   - Confirms successful checkout
   - Updates subscription plan
   - Creates history entry

2. **`invoice.paid`**
   - Records invoice in database
   - Stores amount, PDF link, hosted URL
   
3. **`customer.subscription.updated`**
   - Updates period start/end dates
   - Updates subscription status

### **Features Unlocked Immediately:**

**Basic Plan:**
- ✅ 500 contacts (was 50)
- ✅ 100 companies (was 10)
- ✅ 50 deals/month (was 5)
- ✅ AI Assistant with limited usage
- ✅ Invoice & Offer templates
- ✅ Email generation

---

## 2️⃣ What happens when a payment fails?

### **Stripe's Automatic Retry Logic:**

#### **Initial Failure:**
1. Payment attempt fails (insufficient funds, expired card, etc.)
2. Stripe marks invoice as `past_due`
3. Sends email to customer automatically

#### **Smart Retry Schedule:**
```
Day 0:  Initial attempt fails
Day 3:  First retry
Day 5:  Second retry
Day 7:  Third retry
Day 10: Fourth retry
...continues for up to 4 weeks
```

### **In Your CRM (via Webhooks):**

```python
# Webhook: invoice.payment_failed
def handle_invoice_payment_failed(invoice_data):
    subscription_id = invoice_data.get('subscription')
    
    subscription = Subscription.objects.get(
        stripe_subscription_id=subscription_id
    )
    
    # Mark as past due
    subscription.status = 'past_due'
    subscription.save()
```

### **What User Experiences:**

1. **Immediate:**
   - Status changes to **"Past Due"**
   - Email notification from Stripe
   - Access continues (grace period)

2. **During Retry Period (3-4 weeks):**
   - ⚠️ Warning banner: "Payment failed, please update payment method"
   - Full access continues
   - Multiple retry attempts
   - Email reminders

3. **User Can:**
   - Update payment method in billing portal
   - Stripe auto-retries when new card added
   - Resolve before subscription cancels

### **Access Control:**

```python
# In apps/subscriptions/middleware.py
if subscription.status == 'past_due':
    # Still allow access but show warning
    messages.warning(request, 
        'Your payment failed. Please update your payment method.')
```

### **Automatic Recovery:**

- User updates card → Stripe retries immediately
- Successful payment → Status returns to `active`
- History updated automatically

---

## 3️⃣ What happens if user does not pay next period?

### **End of Retry Period (After ~4 weeks):**

#### **Stripe's Action:**
1. All retry attempts exhausted
2. Subscription cancelled automatically
3. Sends `customer.subscription.deleted` webhook event

#### **In Your CRM:**

```python
# Webhook: customer.subscription.deleted
def handle_subscription_deleted(subscription_data):
    subscription = Subscription.objects.get(
        stripe_subscription_id=subscription_data['id']
    )
    
    old_plan = subscription.plan
    
    # Downgrade to free
    subscription.plan = 'free'
    subscription.status = 'cancelled'
    subscription.stripe_subscription_id = None
    subscription.save()
    
    # Create history entry
    SubscriptionHistory.objects.create(
        user=subscription.user,
        subscription=subscription,
        from_plan=old_plan,
        to_plan='free',
        reason='Subscription ended - payment failed'
    )
```

### **What Happens to User:**

1. **Account Downgraded:**
   - Plan: Basic → **Free**
   - Status: **Cancelled**

2. **Feature Restrictions Applied:**
   ```
   Basic Plan (was):        Free Plan (now):
   ✅ 500 contacts      →   ❌ 50 contacts only
   ✅ 100 companies     →   ❌ 10 companies only
   ✅ 50 deals/month    →   ❌ 5 deals/month
   ✅ AI Assistant      →   ❌ No AI features
   ✅ Full templates    →   ❌ Basic templates only
   ```

3. **Data Preserved:**
   - ✅ All existing contacts kept
   - ✅ All companies preserved
   - ✅ All deals saved
   - ⚠️ Cannot add new beyond free limits
   - ⚠️ Advanced features disabled

4. **User Notifications:**
   - Email: "Your subscription has been cancelled"
   - Dashboard: "Your account has been downgraded to Free"
   - Banner: "Upgrade to access premium features"

### **Grace Period:**

```python
# Optional: Implement grace period
if subscription.status == 'cancelled':
    days_since_cancel = (now() - subscription.updated_at).days
    
    if days_since_cancel <= 7:
        # 7-day grace period
        # Still allow some access to encourage reactivation
        allow_limited_access = True
```

### **Reactivation:**

User can reactivate anytime:
1. Visit `/bg/subscriptions/plans/`
2. Select plan again
3. Enter payment details
4. Full access restored immediately

---

## 4️⃣ What happens if a user upgrades?

### **Upgrade Flow:**

```
Current Plan → Select Higher Plan → Immediate Upgrade → Prorated Billing
```

### **Example: Basic → Pro**

#### **Step 1: User Initiates Upgrade**
- Currently on: **Basic Plan** (€9.99/month)
- Clicks: "Избери Pro" (€29.99/month)

#### **Step 2: Stripe Checkout**
```python
# Same process as new subscription
checkout_session = stripe.checkout.Session.create(
    customer=subscription.stripe_customer_id,  # Existing customer
    payment_method_types=['card'],
    line_items=[{
        'price': settings.STRIPE_PRICE_PRO,  # New price
        'quantity': 1,
    }],
    mode='subscription',
    metadata={
        'user_id': str(request.user.id),
        'plan': 'pro',  # New plan
    }
)
```

#### **Step 3: Stripe Handles Proration**

**Automatic Proration Calculation:**
```
Example (15 days into Basic monthly):
- Basic: €9.99/month (15 days used, 15 days remaining)
- Unused Basic: €9.99 × (15/30) = €4.99 credit

- Pro: €29.99/month (15 days remaining)
- Prorated Pro: €29.99 × (15/30) = €14.99

- Immediate charge: €14.99 - €4.99 = €10.00

Next full charge: €29.99 on original billing date
```

#### **Step 4: Subscription Updated**

```python
# Old subscription modified by Stripe
stripe.Subscription.modify(
    subscription.stripe_subscription_id,
    items=[{
        'id': old_subscription_item_id,
        'price': settings.STRIPE_PRICE_PRO,  # New price
    }],
    proration_behavior='create_prorations'  # Default
)

# In your CRM
subscription.plan = 'pro'
subscription.status = 'active'
# stripe_subscription_id stays the same!
subscription.save()

# History
SubscriptionHistory.objects.create(
    user=request.user,
    subscription=subscription,
    from_plan='basic',
    to_plan='pro',
    reason='User upgraded'
)
```

#### **Step 5: Features Unlocked Immediately**

**Before (Basic):**
- ✅ 500 contacts
- ✅ 100 companies
- ✅ 50 deals/month
- ✅ Limited AI

**After (Pro):**
- ✅ 5,000 contacts ⬆️
- ✅ 1,000 companies ⬆️
- ✅ Unlimited deals ⬆️
- ✅ Full AI features ⬆️
- ✅ Priority support ✨
- ✅ Advanced templates ✨

### **Downgrade (Pro → Basic):**

**Two Options:**

#### **Option 1: Immediate Downgrade**
```python
# Downgrade immediately with credit
subscription.plan = 'basic'
# Prorated credit applied to next invoice
```

#### **Option 2: Schedule at Period End (Recommended)**
```python
# Continue Pro until period ends, then downgrade
subscription.cancel_at_period_end = True
subscription.scheduled_plan = 'basic'
subscription.save()

# User keeps Pro features until billing date
# Then automatically switches to Basic
```

**Current Implementation:** Uses Option 1 (immediate)

### **What Gets Charged:**

```python
# Upgrade invoice breakdown:
{
    "description": "Subscription upgrade",
    "lines": [
        {
            "description": "Unused time on Basic (15 days)",
            "amount": -499,  # €4.99 credit
        },
        {
            "description": "Remaining time on Pro (15 days)",
            "amount": 1499,  # €14.99 charge
        }
    ],
    "total": 1000,  # €10.00 net charge
}
```

---

## 🔧 Technical Implementation Details

### **Database Schema:**

```python
class Subscription(models.Model):
    user = models.OneToOneField(User)
    plan = models.CharField(max_length=20)  # free, basic, pro, enterprise
    status = models.CharField(max_length=20)  # active, past_due, cancelled
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubscriptionHistory(models.Model):
    user = models.ForeignKey(User)
    subscription = models.ForeignKey(Subscription)
    from_plan = models.CharField(max_length=20)
    to_plan = models.CharField(max_length=20)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### **Webhook Endpoints:**

```python
# URL: /subscriptions/webhook/
# Method: POST
# Authentication: Stripe signature verification

@csrf_exempt
def stripe_webhook(request):
    event = stripe.Webhook.construct_event(
        payload=request.body,
        sig_header=request.META['HTTP_STRIPE_SIGNATURE'],
        secret=settings.STRIPE_WEBHOOK_SECRET
    )
    
    handlers = {
        'checkout.session.completed': handle_checkout_session_completed,
        'invoice.paid': handle_invoice_paid,
        'invoice.payment_failed': handle_invoice_payment_failed,
        'customer.subscription.updated': handle_subscription_updated,
        'customer.subscription.deleted': handle_subscription_deleted,
    }
    
    handler = handlers.get(event['type'])
    if handler:
        handler(event['data']['object'])
    
    return HttpResponse(status=200)
```

### **Middleware for Access Control:**

```python
# In apps/subscriptions/middleware.py

class SubscriptionMiddleware:
    def __call__(self, request):
        if request.user.is_authenticated:
            subscription = request.user.subscription
            plan_config = subscription.get_plan_config()
            
            # Add to request context
            request.subscription = subscription
            request.plan_limits = plan_config['limits']
            
            # Check if over limits
            if subscription.is_over_limit('contacts'):
                messages.warning(request, 
                    'You have reached your contact limit. Upgrade to add more.')
        
        return self.get_response(request)
```

---

## 📊 Plan Limits

### **Free Plan:**
```python
{
    'name': 'Free',
    'price': 0,
    'limits': {
        'contacts': 50,
        'companies': 10,
        'deals_per_month': 5,
        'ai_requests_per_month': 0,
        'storage_mb': 100,
    },
    'features': {
        'crm': True,
        'ai_assistant': False,
        'templates': 'basic',
        'support': 'community',
    }
}
```

### **Basic Plan (€9.99/month):**
```python
{
    'name': 'Basic',
    'price': 9.99,
    'limits': {
        'contacts': 500,
        'companies': 100,
        'deals_per_month': 50,
        'ai_requests_per_month': 100,
        'storage_mb': 1024,
    },
    'features': {
        'crm': True,
        'ai_assistant': True,
        'templates': 'standard',
        'support': 'email',
    }
}
```

### **Pro Plan (€29.99/month):**
```python
{
    'name': 'Pro',
    'price': 29.99,
    'limits': {
        'contacts': 5000,
        'companies': 1000,
        'deals_per_month': -1,  # Unlimited
        'ai_requests_per_month': 500,
        'storage_mb': 5120,
    },
    'features': {
        'crm': True,
        'ai_assistant': True,
        'templates': 'all',
        'support': 'priority',
        'api_access': True,
    }
}
```

### **Enterprise Plan (€99.99/month):**
```python
{
    'name': 'Enterprise',
    'price': 99.99,
    'limits': {
        'contacts': -1,  # Unlimited
        'companies': -1,  # Unlimited
        'deals_per_month': -1,  # Unlimited
        'ai_requests_per_month': -1,  # Unlimited
        'storage_mb': -1,  # Unlimited
    },
    'features': {
        'crm': True,
        'ai_assistant': True,
        'templates': 'all',
        'support': 'dedicated',
        'api_access': True,
        'custom_integrations': True,
        'white_label': True,
    }
}
```

---

## 🔄 Sync Commands

### **Manual Sync from Stripe:**

```bash
# Sync all subscriptions
python manage.py sync_stripe_subscriptions

# Output:
# 🔄 Syncing Subscriptions from Stripe
# Found 5 users with Stripe customers
# ✅ Updated user@example.com: free → basic
# ✅ Sync complete! Updated 1 subscription(s)
```

### **Setup Stripe Products:**

```bash
# Create products and update .env
python manage.py setup_stripe

# Output:
# 🔧 Stripe Products Setup
# 1️⃣  Creating Free Plan... ✅
# 2️⃣  Creating Basic Plan... ✅
# 3️⃣  Creating Pro Plan... ✅
# 4️⃣  Creating Enterprise Plan... ✅
# 📝 Updating .env file... ✅
# 🎉 Setup Complete!
```

---

## ✅ Summary

### **Payment Success:**
- ✅ Immediate plan activation
- ✅ Features unlocked instantly
- ✅ History recorded
- ✅ Confirmation message

### **Payment Failure:**
- ⚠️ Status: `past_due`
- ⏳ Grace period with access
- 🔄 Auto-retry for 3-4 weeks
- 📧 Email notifications

### **Non-Payment:**
- ❌ Downgrade to Free after retries
- 💾 Data preserved
- 🔒 Features restricted
- ♻️ Can reactivate anytime

### **Upgrade:**
- ⚡ Immediate upgrade
- 💰 Prorated billing
- ✨ Features unlocked instantly
- 📊 History tracked

---

## 🚀 Production Checklist

Before going live:

- [ ] Configure Stripe webhooks in dashboard
- [ ] Set webhook secret in `.env`
- [ ] Test all payment scenarios
- [ ] Test webhook events
- [ ] Configure email notifications
- [ ] Set up monitoring for failed payments
- [ ] Create dunning workflow (payment reminders)
- [ ] Add customer billing portal
- [ ] Test proration calculations
- [ ] Configure tax settings (if needed)
- [ ] Set up invoice emails
- [ ] Test cancellation flow
- [ ] Document customer support procedures

---

**Last Updated:** October 5, 2025  
**Version:** 1.0  
**Author:** Django CRM Team
