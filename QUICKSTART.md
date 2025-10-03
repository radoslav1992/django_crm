# Quick Start Guide

Get your Django CRM up and running in 5 minutes!

## Prerequisites

- Python 3.10+
- pip
- virtualenv

## Quick Setup

### 1. Run the setup script (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Create a virtual environment
- Install dependencies
- Set up the database
- Create a superuser
- Collect static files
- Create default CRM data

### 2. Manual Setup (Alternative)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 3. Configure Environment Variables

Edit `.env` file with your settings:

```env
# Required for production
SECRET_KEY=your-secret-key-here
DEBUG=True

# Stripe (for subscriptions)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Gemini AI (for AI features)
GEMINI_API_KEY=your-gemini-api-key
```

### 4. Start the Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

### 5. (Optional) Start Background Workers

In separate terminal windows:

```bash
# Celery worker
celery -A config worker -l info

# Celery beat (scheduled tasks)
celery -A config beat -l info
```

## First Steps

1. **Login** with your superuser account
2. **Update Profile** - Go to Profile and fill in your company details
3. **Configure Stripe** - Add your Stripe keys in Settings → Stripe Settings
4. **Create Pipeline** - Set up your sales pipeline stages
5. **Add Contacts** - Start adding contacts and companies
6. **Try AI Assistant** - Chat with the AI assistant for help

## Free Trial

The system starts with a **FREE plan** that includes:
- 100 contacts
- 1 user
- 10 AI requests per month
- Basic CRM features
- Basic templates

## Upgrade Plans

Upgrade to unlock more features:

| Plan | Price | Contacts | AI Requests |
|------|-------|----------|-------------|
| Free | €0 | 100 | 10/month |
| Basic | €29/month | 1,000 | 100/month |
| Pro | €99/month | 10,000 | 500/month |
| Enterprise | €299/month | Unlimited | Unlimited |

## Getting Stripe API Keys

1. Go to https://stripe.com and create an account
2. Navigate to Developers → API Keys
3. Copy your **Publishable key** (starts with `pk_`)
4. Copy your **Secret key** (starts with `sk_`)
5. Add them to your `.env` file

### Create Subscription Products

1. Go to Stripe Dashboard → Products
2. Create products for each plan:
   - Basic: €29/month
   - Pro: €99/month
   - Enterprise: €299/month
3. Copy the Price IDs and add to `.env`

### Configure Webhooks

1. Go to Developers → Webhooks
2. Add endpoint: `https://yourdomain.com/subscriptions/webhook/`
3. Select these events:
   - `checkout.session.completed`
   - `invoice.paid`
   - `invoice.payment_failed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
4. Copy the webhook secret and add to `.env`

## Getting Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key and add to `.env`

## Common Issues

### Redis Connection Error

If you see Redis errors and don't need background tasks:
- Comment out Celery tasks
- Or install and start Redis:
  ```bash
  # macOS
  brew install redis
  brew services start redis
  
  # Ubuntu
  sudo apt install redis-server
  sudo service redis-server start
  ```

### Database Errors

Reset the database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading

Collect static files again:
```bash
python manage.py collectstatic --noinput
```

## Need Help?

- Check the full README.md
- Review the code documentation
- Check Django documentation: https://docs.djangoproject.com/

## Production Deployment

For production deployment:
1. Set `DEBUG=False`
2. Change `SECRET_KEY`
3. Set proper `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Configure proper email backend
6. Set up HTTPS
7. Use a production WSGI server (Gunicorn)
8. Set up a reverse proxy (Nginx)

Example production start:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

**Enjoy your CRM!** 🎉

