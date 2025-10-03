#!/bin/bash

# Django CRM Setup Script
echo "======================================"
echo "Django CRM Setup"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration (Stripe keys, Gemini API key, etc.)"
else
    echo ""
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p media/avatars media/invoices media/templates staticfiles

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "======================================"
echo "Create Superuser Account"
echo "======================================"
read -p "Would you like to create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create default pipeline and stages (optional)
echo ""
echo "Creating default CRM data..."
python manage.py shell << EOF
from apps.accounts.models import User
from apps.crm.models import Pipeline, Stage

# Get first superuser
user = User.objects.filter(is_superuser=True).first()

if user:
    # Create default pipeline
    pipeline, created = Pipeline.objects.get_or_create(
        owner=user,
        name='Sales Pipeline',
        defaults={'is_default': True}
    )
    
    if created:
        # Create default stages
        Stage.objects.create(pipeline=pipeline, name='Lead', probability=10, order=1)
        Stage.objects.create(pipeline=pipeline, name='Qualified', probability=25, order=2)
        Stage.objects.create(pipeline=pipeline, name='Proposal', probability=50, order=3)
        Stage.objects.create(pipeline=pipeline, name='Negotiation', probability=75, order=4)
        Stage.objects.create(pipeline=pipeline, name='Closed Won', probability=100, order=5)
        print('✓ Default pipeline created')
    else:
        print('✓ Pipeline already exists')
else:
    print('⚠️  No superuser found. Create one and run this again.')
EOF

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - STRIPE_PUBLISHABLE_KEY"
echo "   - STRIPE_SECRET_KEY"
echo "   - GEMINI_API_KEY"
echo ""
echo "2. Create Stripe products and update .env with price IDs"
echo ""
echo "3. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "4. (Optional) Start Celery worker for background tasks:"
echo "   celery -A config worker -l info"
echo ""
echo "5. (Optional) Start Celery beat for scheduled tasks:"
echo "   celery -A config beat -l info"
echo ""
echo "6. Visit: http://127.0.0.1:8000"
echo ""
echo "======================================"
echo "Happy CRM-ing! 🚀"
echo "======================================"

