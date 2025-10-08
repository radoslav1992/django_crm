#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         SSL FIX + INSTALL DEPENDENCIES                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Fix SSL certificates
echo "🔧 Installing Python SSL certificates..."
/Applications/Python\ 3.12/Install\ Certificates.command

echo ""
echo "✅ SSL certificates installed!"
echo ""

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
cd /Users/I567283/personal/django_crm
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                   INSTALLATION COMPLETE                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "✅ All packages installed including resend==0.8.0"
echo ""
echo "🚀 Next steps:"
echo "   1. python manage.py runserver"
echo "   2. Visit: http://localhost:8000/accounts/resend-settings/"
echo ""

