# 🔧 Stripe Subscription Setup Guide

## ❌ Current Error

**Error:** `No such price: 'price_basic_monthly'`

**Reason:** The price IDs in your `.env` file are placeholders. You need to create actual products and prices in your Stripe account.

---

## 📋 Step-by-Step Setup

### **Step 1: Login to Stripe Dashboard**

1. Go to: https://dashboard.stripe.com/
2. Login with your account
3. Make sure you're in **Test Mode** (toggle in top right)

---

### **Step 2: Create Products and Prices**

#### **Option A: Using Stripe Dashboard (Recommended)**

1. **Go to Products:**
   - Visit: https://dashboard.stripe.com/test/products
   - Or: Click **Products** in the left sidebar

2. **Create Free Plan:**
   - Click **+ Add product**
   - Name: `Free Plan`
   - Description: `Free CRM features`
   - Pricing model: **Standard pricing**
   - Price: `0.00 EUR`
   - Billing period: **Monthly**
   - Click **Save product**
   - **COPY THE PRICE ID** (starts with `price_`)

3. **Create Basic Plan:**
   - Click **+ Add product**
   - Name: `Basic Plan`
   - Description: `Essential CRM features with AI`
   - Pricing model: **Standard pricing**
   - Price: `9.99 EUR` (or your preferred price)
   - Billing period: **Monthly**
   - Click **Save product**
   - **COPY THE PRICE ID** (starts with `price_`)

4. **Create Pro Plan:**
   - Click **+ Add product**
   - Name: `Pro Plan`
   - Description: `Advanced CRM with unlimited features`
   - Pricing model: **Standard pricing**
   - Price: `29.99 EUR` (or your preferred price)
   - Billing period: **Monthly**
   - Click **Save product**
   - **COPY THE PRICE ID** (starts with `price_`)

5. **Create Enterprise Plan:**
   - Click **+ Add product**
   - Name: `Enterprise Plan`
   - Description: `Full-featured CRM for large teams`
   - Pricing model: **Standard pricing**
   - Price: `99.99 EUR` (or your preferred price)
   - Billing period: **Monthly**
   - Click **Save product**
   - **COPY THE PRICE ID** (starts with `price_`)

---

#### **Option B: Using Stripe CLI (Faster)**

```bash
# Install Stripe CLI (if not already installed)
# Mac:
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Create Free Plan
stripe products create \
  --name="Free Plan" \
  --description="Free CRM features"

# Get the product ID from output, then create price
stripe prices create \
  --product=prod_XXXXX \
  --unit-amount=0 \
  --currency=eur \
  --recurring[interval]=month

# Create Basic Plan (€9.99/month)
stripe products create \
  --name="Basic Plan" \
  --description="Essential CRM features with AI"

stripe prices create \
  --product=prod_XXXXX \
  --unit-amount=999 \
  --currency=eur \
  --recurring[interval]=month

# Create Pro Plan (€29.99/month)
stripe products create \
  --name="Pro Plan" \
  --description="Advanced CRM with unlimited features"

stripe prices create \
  --product=prod_XXXXX \
  --unit-amount=2999 \
  --currency=eur \
  --recurring[interval]=month

# Create Enterprise Plan (€99.99/month)
stripe products create \
  --name="Enterprise Plan" \
  --description="Full-featured CRM for large teams"

stripe prices create \
  --product=prod_XXXXX \
  --unit-amount=9999 \
  --currency=eur \
  --recurring[interval]=month
```

---

### **Step 3: Update .env File**

After creating the products, you'll have 4 price IDs. Update your `.env` file:

```bash
# Open .env file
nano .env
```

Replace the placeholder price IDs with your actual Stripe price IDs:

```env
# OLD (Placeholders):
STRIPE_PRICE_FREE=price_free_plan
STRIPE_PRICE_BASIC=price_basic_monthly
STRIPE_PRICE_PRO=price_pro_monthly
STRIPE_PRICE_ENTERPRISE=price_enterprise_monthly

# NEW (Your actual IDs from Stripe):
STRIPE_PRICE_FREE=price_1aBcDeFgHiJkLmNoP
STRIPE_PRICE_BASIC=price_2qRsTuVwXyZaBcDeF
STRIPE_PRICE_PRO=price_3gHiJkLmNoPqRsTuV
STRIPE_PRICE_ENTERPRISE=price_4wXyZaBcDeFgHiJkL
```

**Your Stripe API Keys look correct, but verify:**
- Test Publishable Key: `pk_test_...`
- Test Secret Key: `sk_test_...`

---

### **Step 4: Restart the Server**

```bash
# Stop the server
Ctrl+C

# Restart
cd /Users/I567283/personal/django_crm
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001
```

---

## 🎯 Quick Reference

### **What Each Plan Includes (as configured in code):**

#### **Free Plan (€0/month):**
- ✅ 50 contacts
- ✅ 10 companies
- ✅ 5 deals/month
- ✅ Basic CRM features
- ❌ No AI features

#### **Basic Plan (€9.99/month suggested):**
- ✅ 500 contacts
- ✅ 100 companies
- ✅ 50 deals/month
- ✅ AI Assistant (limited)
- ✅ Invoice templates
- ✅ Email support

#### **Pro Plan (€29.99/month suggested):**
- ✅ 5,000 contacts
- ✅ 1,000 companies
- ✅ Unlimited deals
- ✅ Full AI features
- ✅ All templates
- ✅ Priority support

#### **Enterprise Plan (€99.99/month suggested):**
- ✅ Unlimited everything
- ✅ Advanced AI features
- ✅ Custom templates
- ✅ Dedicated support
- ✅ API access

---

## 🔍 Find Your Price IDs

### **In Stripe Dashboard:**

1. Go to: https://dashboard.stripe.com/test/products
2. Click on a product
3. Under "Pricing", you'll see the Price ID
4. Example: `price_1OAbCdEfGhIjKlMn`

### **Price ID Format:**
- Test mode: `price_1...` (starts with `price_1`)
- Live mode: `price_1...` (same format)

---

## ⚠️ Important Notes

### **Test Mode vs Live Mode:**

**Test Mode** (current):
- Use test API keys (pk_test_... and sk_test_...)
- Use test price IDs
- No real money charged
- Use test card: `4242 4242 4242 4242`

**Live Mode** (production):
- Use live API keys (pk_live_... and sk_live_...)
- Use live price IDs
- Real money charged
- Real credit cards

### **Free Plan Consideration:**

For the free plan, you have two options:

**Option 1: Price with €0**
- Create a price with `0.00 EUR`
- Users can "subscribe" but pay nothing

**Option 2: No Stripe subscription**
- Don't use Stripe for free plan
- Just mark user as free tier in database
- Skip payment flow entirely

Currently, the code expects a price ID even for free. If you want to skip Stripe for free users, let me know and I can modify the code.

---

## 🧪 Test Your Setup

### **After updating .env:**

1. **Visit plans page:**
   ```
   http://localhost:8001/bg/subscriptions/plans/
   ```

2. **Try subscribing to Basic:**
   - Click "Избери Basic"
   - You should see Stripe checkout page
   - Use test card: `4242 4242 4242 4242`
   - Any future date for expiry
   - Any 3-digit CVC

3. **Successful payment:**
   - You'll be redirected back
   - Your subscription will be active
   - Features will be unlocked

---

## 🐛 Troubleshooting

### **Error: "No such price"**
- ✅ Check you copied the correct price ID from Stripe
- ✅ Make sure you're in test mode
- ✅ Verify .env file has correct price IDs
- ✅ Restart server after changing .env

### **Error: "No such customer"**
- ✅ Check STRIPE_SECRET_KEY is correct
- ✅ Make sure you're using test keys with test price IDs

### **Error: "Invalid API Key"**
- ✅ Verify STRIPE_SECRET_KEY starts with `sk_test_`
- ✅ Check for extra spaces in .env file
- ✅ Generate new key from Stripe dashboard if needed

---

## 📚 Additional Resources

- **Stripe Products:** https://dashboard.stripe.com/test/products
- **Stripe API Keys:** https://dashboard.stripe.com/test/apikeys
- **Stripe Testing:** https://stripe.com/docs/testing
- **Stripe Checkout:** https://stripe.com/docs/checkout

---

## ✅ Checklist

- [ ] Created Free Plan in Stripe
- [ ] Created Basic Plan in Stripe
- [ ] Created Pro Plan in Stripe
- [ ] Created Enterprise Plan in Stripe
- [ ] Copied all 4 price IDs
- [ ] Updated .env file with real price IDs
- [ ] Restarted Django server
- [ ] Tested subscription checkout
- [ ] Successfully subscribed to a plan

---

## 🎉 Once Setup is Complete

Your users will be able to:
- ✅ View subscription plans
- ✅ Subscribe to any plan
- ✅ Pay securely with Stripe
- ✅ Features automatically unlocked
- ✅ Upgrade/downgrade anytime
- ✅ Cancel subscriptions
- ✅ View invoices

**Your CRM will be fully functional with Stripe subscriptions!** 🚀
