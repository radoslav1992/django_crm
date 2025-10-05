#!/bin/bash

# Stripe Products Setup Script for Django CRM
# This script helps you create subscription products in Stripe

echo "🔧 Stripe Products Setup for Django CRM"
echo "========================================"
echo ""

# Check if Stripe CLI is installed
if ! command -v stripe &> /dev/null; then
    echo "❌ Stripe CLI is not installed."
    echo ""
    echo "📦 Install Stripe CLI:"
    echo "   Mac: brew install stripe/stripe-cli/stripe"
    echo "   Other: https://stripe.com/docs/stripe-cli"
    echo ""
    exit 1
fi

echo "✅ Stripe CLI found"
echo ""

# Check if logged in
if ! stripe config --list &> /dev/null; then
    echo "🔐 Please login to Stripe CLI first:"
    echo "   Run: stripe login"
    echo ""
    exit 1
fi

echo "✅ Logged in to Stripe"
echo ""
echo "📝 Creating subscription products in TEST mode..."
echo ""

# Create Free Plan
echo "1️⃣ Creating Free Plan (€0/month)..."
FREE_PRODUCT=$(stripe products create \
  --name="Free Plan" \
  --description="Free CRM features - 50 contacts, 10 companies, 5 deals/month" \
  --format=json | jq -r '.id')

if [ -z "$FREE_PRODUCT" ]; then
    echo "❌ Failed to create Free product"
    exit 1
fi

FREE_PRICE=$(stripe prices create \
  --product="$FREE_PRODUCT" \
  --unit-amount=0 \
  --currency=eur \
  --recurring[interval]=month \
  --format=json | jq -r '.id')

echo "   ✅ Free Plan created: $FREE_PRICE"
echo ""

# Create Basic Plan
echo "2️⃣ Creating Basic Plan (€9.99/month)..."
BASIC_PRODUCT=$(stripe products create \
  --name="Basic Plan" \
  --description="Essential CRM with AI - 500 contacts, 100 companies, 50 deals/month" \
  --format=json | jq -r '.id')

BASIC_PRICE=$(stripe prices create \
  --product="$BASIC_PRODUCT" \
  --unit-amount=999 \
  --currency=eur \
  --recurring[interval]=month \
  --format=json | jq -r '.id')

echo "   ✅ Basic Plan created: $BASIC_PRICE"
echo ""

# Create Pro Plan
echo "3️⃣ Creating Pro Plan (€29.99/month)..."
PRO_PRODUCT=$(stripe products create \
  --name="Pro Plan" \
  --description="Advanced CRM - 5,000 contacts, 1,000 companies, unlimited deals" \
  --format=json | jq -r '.id')

PRO_PRICE=$(stripe prices create \
  --product="$PRO_PRODUCT" \
  --unit-amount=2999 \
  --currency=eur \
  --recurring[interval]=month \
  --format=json | jq -r '.id')

echo "   ✅ Pro Plan created: $PRO_PRICE"
echo ""

# Create Enterprise Plan
echo "4️⃣ Creating Enterprise Plan (€99.99/month)..."
ENTERPRISE_PRODUCT=$(stripe products create \
  --name="Enterprise Plan" \
  --description="Full-featured CRM - Unlimited everything with dedicated support" \
  --format=json | jq -r '.id')

ENTERPRISE_PRICE=$(stripe prices create \
  --product="$ENTERPRISE_PRODUCT" \
  --unit-amount=9999 \
  --currency=eur \
  --recurring[interval]=month \
  --format=json | jq -r '.id')

echo "   ✅ Enterprise Plan created: $ENTERPRISE_PRICE"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All products created successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Your Price IDs:"
echo ""
echo "STRIPE_PRICE_FREE=$FREE_PRICE"
echo "STRIPE_PRICE_BASIC=$BASIC_PRICE"
echo "STRIPE_PRICE_PRO=$PRO_PRICE"
echo "STRIPE_PRICE_ENTERPRISE=$ENTERPRISE_PRICE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Update your .env file with these price IDs:"
echo "   nano .env"
echo ""
echo "2. Replace the placeholder price IDs with the ones above"
echo ""
echo "3. Restart your Django server:"
echo "   python manage.py runserver 0.0.0.0:8001"
echo ""
echo "4. Test subscriptions at:"
echo "   http://localhost:8001/bg/subscriptions/plans/"
echo ""
echo "5. Use test card: 4242 4242 4242 4242"
echo ""
echo "🎉 Done! Your Stripe subscriptions are ready!"
