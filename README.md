# Django CRM System

A comprehensive CRM (Customer Relationship Management) system built with Django, featuring AI-powered assistance, invoice management, and multi-tier subscriptions.

## 🌟 Features

### Core CRM Features
- **Contact Management**: Organize contacts with full details, company associations, and custom fields
- **Company Management**: Track companies with industry info, revenue data, and relationships
- **Deal Pipeline**: Manage sales deals through customizable pipeline stages
- **Task Management**: Create and track tasks with priorities and due dates
- **Activity Logging**: Automatic activity tracking for all CRM interactions

### Invoice & Offer Management
- **Invoice Creation**: Generate professional invoices with line items
- **Offer/Quote System**: Create offers that can be converted to invoices
- **QR Code Payments**: Automatic QR code generation for Stripe payment links
- **Payment Tracking**: Automatic matching of payments to invoices
- **Template Studio**: Visual editor for creating custom invoice/offer templates

### AI Assistant (Gemini 2.5 Flash-Lite)
- **Smart Chat**: AI-powered assistant for CRM guidance (Gemini 2.5 Flash-Lite)
- **Email Generation**: Auto-generate professional emails for contacts
- **Deal Analysis**: AI insights and recommendations for deals
- **Task Suggestions**: Intelligent task recommendations
- **Template Content**: AI-generated content for invoice/offer templates
- **Cost Optimized**: Using Flash-Lite for better price-performance

### Subscription & Payments
- **Stripe Integration**: Secure payment processing for subscriptions
- **Multi-tier Plans**: Free, Basic, Pro, and Enterprise plans
- **EUR Currency**: All pricing in Euros
- **Usage Limits**: Automatic enforcement of plan limits
- **User Stripe Keys**: Each user can configure their own Stripe keys for customer payments

### Multilingual Support
- **Bulgarian (Primary)**: Full Bulgarian language support
- **English (Secondary)**: Complete English translation
- **Easy Switching**: User can choose preferred language

## 📋 Requirements

- Python 3.10+
- PostgreSQL (recommended) or SQLite (development)
- Redis (for Celery tasks)
- Stripe Account (for subscriptions)
- Gemini API Key (for AI features)

## 🚀 Installation

### 1. Clone the Repository

```bash
cd django_crm
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Stripe Price IDs (create these in Stripe Dashboard)
STRIPE_PRICE_BASIC=price_xxxx
STRIPE_PRICE_PRO=price_xxxx
STRIPE_PRICE_ENTERPRISE=price_xxxx

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Language
LANGUAGE_CODE=bg
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 8. Create Translation Files (Optional)

```bash
python manage.py makemessages -l bg
python manage.py compilemessages
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## 🔄 Running Background Tasks

Start Celery worker for async tasks:

```bash
celery -A config worker -l info
```

Start Celery beat for scheduled tasks:

```bash
celery -A config beat -l info
```

## 💳 Stripe Setup

### 1. Create Stripe Account
- Sign up at https://stripe.com
- Get your API keys from the Dashboard

### 2. Create Products and Prices
Create subscription products in Stripe Dashboard:
- **Basic Plan**: €29/month
- **Pro Plan**: €99/month
- **Enterprise Plan**: €299/month

### 3. Configure Webhooks
Add webhook endpoint: `https://yourdomain.com/subscriptions/webhook/`

Select events:
- `checkout.session.completed`
- `invoice.paid`
- `invoice.payment_failed`
- `customer.subscription.updated`
- `customer.subscription.deleted`

### 4. User Stripe Keys
Users can configure their own Stripe keys in Settings → Stripe Settings to accept payments from their customers.

## 🤖 Gemini AI Setup

### 1. Get API Key
- Visit https://makersuite.google.com/app/apikey
- Create a new API key

### 2. Configure in .env
```env
GEMINI_API_KEY=your-api-key-here
```

### 3. AI Features
- Chat assistant for CRM guidance
- Email draft generation
- Deal analysis and insights
- Task suggestions
- Template content generation

## 📊 Subscription Plans

| Feature | Free | Basic | Pro | Enterprise |
|---------|------|-------|-----|------------|
| **Price** | €0 | €29/mo | €99/mo | €299/mo |
| **Contacts** | 100 | 1,000 | 10,000 | Unlimited |
| **Users** | 1 | 3 | 10 | Unlimited |
| **AI Requests/mo** | 10 | 100 | 500 | Unlimited |
| **Basic CRM** | ✓ | ✓ | ✓ | ✓ |
| **Templates** | Basic | Advanced | Advanced | Advanced |
| **Email Integration** | ✗ | ✓ | ✓ | ✓ |
| **AI Assistant** | Limited | Basic | Advanced | Advanced |
| **Custom Fields** | ✗ | ✗ | ✓ | ✓ |
| **API Access** | ✗ | ✗ | ✓ | ✓ |
| **Priority Support** | ✗ | ✗ | ✗ | ✓ |
| **White Label** | ✗ | ✗ | ✗ | ✓ |

## 🏗️ Project Structure

```
django_crm/
├── apps/
│   ├── accounts/          # User authentication & profiles
│   ├── crm/              # Core CRM (contacts, companies, deals)
│   ├── invoices/         # Invoice & offer management
│   ├── templates/        # Document template studio
│   ├── subscriptions/    # Stripe subscription management
│   └── ai_assistant/     # Gemini AI integration
├── config/               # Django settings & configuration
├── templates/            # HTML templates
├── static/              # CSS, JS, images
├── media/               # User uploads
├── locale/              # Translation files
└── manage.py
```

## 🔧 Configuration

### Multi-language Support
Change default language in `config/settings.py`:
```python
LANGUAGE_CODE = 'bg'  # or 'en'
```

### Subscription Limits
Configure plan limits in `config/settings.py`:
```python
SUBSCRIPTION_PLANS = {
    'free': {
        'contacts_limit': 100,
        'users_limit': 1,
        'ai_requests_per_month': 10,
        ...
    },
    ...
}
```

## 📱 Key Functionality

### Automatic Payment Matching
The system automatically matches incoming payments to invoices based on:
- Amount matching
- Currency matching
- Invoice status
- Payment reference

Celery task runs daily to match unmatched payments.

### QR Code Generation
When you add a Stripe payment URL to an invoice:
1. QR code is automatically generated
2. Customers can scan to pay
3. Payments are tracked and matched

### AI Assistant Usage
- Track usage per subscription plan
- Automatic monthly reset
- Soft limit enforcement (users get warnings)

### Template Studio
Visual editor for creating:
- Invoice templates
- Offer templates
- Custom header/footer
- Color schemes
- Logo upload
- Custom CSS

## 🌐 Deployment

### Production Settings
1. Set `DEBUG=False`
2. Configure proper `ALLOWED_HOSTS`
3. Use PostgreSQL database
4. Set up proper `SECRET_KEY`
5. Configure email backend
6. Set up HTTPS
7. Configure Stripe webhook with production URL

### Recommended Stack
- **Web Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery + Redis
- **Static Files**: WhiteNoise or CDN

### Environment Variables (Production)
```env
DEBUG=False
SECRET_KEY=generate-strong-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

## 🧪 Testing

```bash
python manage.py test
```

## 📝 License

This project is proprietary software. All rights reserved.

## 🤝 Support

For support and questions:
- Check documentation in `/docs`
- Contact support team
- Visit admin panel for system settings

## 🔐 Security

- All passwords are hashed using Django's built-in authentication
- Stripe keys are stored securely
- CSRF protection enabled
- XSS protection via Django templates
- SQL injection prevention via ORM
- Regular security updates

## 📈 Analytics & Monitoring

The system tracks:
- User activity
- Subscription usage
- AI request consumption
- Payment processing
- Invoice generation

## 🌍 Internationalization

Supported languages:
- Bulgarian (bg) - Primary
- English (en) - Secondary

To add new translations:
```bash
python manage.py makemessages -l <language_code>
# Edit .po files
python manage.py compilemessages
```

## 🔄 Database Migrations

When models change:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📦 Dependencies

Key packages:
- Django 4.2.7
- Stripe 7.4.0
- Google Generative AI 0.3.2
- Celery 5.3.4
- Pillow 10.1.0
- QRCode 7.4.2
- ReportLab 4.0.7

See `requirements.txt` for full list.

## 🎯 Roadmap

Upcoming features:
- [ ] Email campaign management
- [ ] Advanced reporting & analytics
- [ ] Mobile app
- [ ] API documentation
- [ ] Zapier integration
- [ ] Calendar integration
- [ ] WhatsApp integration
- [ ] Advanced workflow automation

## 👥 Credits

Built with Django and powered by:
- Stripe for payments
- Gemini AI for intelligence
- Bootstrap for UI
- PostgreSQL for data

---

**Version**: 1.0.0  
**Last Updated**: October 2025

