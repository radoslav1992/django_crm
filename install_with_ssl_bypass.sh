#!/bin/bash
echo "Installing packages with SSL bypass..."
cd /Users/I567283/personal/django_crm
source venv/bin/activate
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org certifi==2024.2.2 urllib3==2.2.1 resend==0.8.0
echo ""
echo "✅ Installation complete!"
echo ""
echo "Now restart your Django server:"
echo "1. Stop current server (Ctrl+C)"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000/templates/studio/"
echo ""
