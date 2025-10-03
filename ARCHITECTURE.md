# System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Django CRM System                        │
│                    (Bulgarian & English Support)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   Frontend   │      │   Backend    │     │  External    │
│  Bootstrap 5 │◄────►│    Django    │◄───►│  Services    │
│   Templates  │      │     Apps     │     │              │
└──────────────┘      └──────────────┘     └──────────────┘
                              │                     │
                              │                     ├─ Stripe API
                              │                     ├─ Gemini AI API
                              ▼                     └─ Redis
                      ┌──────────────┐
                      │   Database   │
                      │  PostgreSQL  │
                      │  or SQLite   │
                      └──────────────┘
```

## 📦 Application Structure

### 1. Accounts App (User Management)
```
accounts/
├── models.py
│   ├── User (Custom user model)
│   │   ├── Authentication fields
│   │   ├── Profile information
│   │   ├── Company details
│   │   ├── Stripe keys (for user's customers)
│   │   └── Preferences (language, timezone)
│   └── TeamMember (Multi-user support)
│       ├── User reference
│       ├── Organization reference
│       ├── Role (Owner, Admin, Manager, User)
│       └── Permissions
├── views.py
│   ├── register()
│   ├── login()
│   ├── logout()
│   ├── profile()
│   ├── stripe_settings()
│   └── landing_page()
├── forms.py
│   ├── UserRegistrationForm
│   ├── UserLoginForm
│   ├── UserProfileForm
│   └── StripeSettingsForm
└── urls.py
```

### 2. CRM App (Core Functionality)
```
crm/
├── models.py
│   ├── Contact
│   │   ├── Personal information
│   │   ├── Company association
│   │   ├── Social media links
│   │   └── Tags
│   ├── Company
│   │   ├── Company details
│   │   ├── Industry & size
│   │   └── Financial info
│   ├── Pipeline
│   │   └── Custom sales pipelines
│   ├── Stage
│   │   ├── Pipeline stages
│   │   └── Win probabilities
│   ├── Deal
│   │   ├── Deal details
│   │   ├── Pipeline & stage
│   │   ├── Value & currency
│   │   └── Status tracking
│   ├── Task
│   │   ├── Task details
│   │   ├── Priority & type
│   │   ├── Due date
│   │   └── Assignment
│   ├── Activity
│   │   ├── Activity logging
│   │   └── Timeline tracking
│   └── CustomField
│       ├── Field definitions
│       └── Entity associations
├── views.py
│   ├── dashboard()
│   ├── contact_* (CRUD operations)
│   ├── company_* (CRUD operations)
│   ├── deal_* (CRUD operations)
│   ├── task_* (CRUD operations)
│   └── pipeline_* (CRUD operations)
└── forms.py
    ├── ContactForm
    ├── CompanyForm
    ├── DealForm
    ├── TaskForm
    └── PipelineForm
```

### 3. Invoices App (Financial Management)
```
invoices/
├── models.py
│   ├── Invoice
│   │   ├── Invoice details
│   │   ├── Client information
│   │   ├── Financial calculations
│   │   ├── Status tracking
│   │   ├── QR code
│   │   └── Payment URL
│   ├── InvoiceItem
│   │   ├── Line items
│   │   └── Calculations
│   ├── Offer
│   │   ├── Offer details
│   │   ├── Valid until date
│   │   └── Conversion to invoice
│   ├── OfferItem
│   │   ├── Line items
│   │   └── Calculations
│   └── Payment
│       ├── Payment details
│       ├── Stripe integration
│       ├── Invoice matching
│       └── Payment methods
├── views.py
│   ├── invoice_* (CRUD operations)
│   ├── invoice_pdf()
│   ├── offer_* (CRUD operations)
│   ├── offer_convert_to_invoice()
│   └── payment_* (Create & list)
├── tasks.py (Celery)
│   ├── match_payments_with_invoices()
│   ├── send_payment_reminders()
│   └── generate_invoice_qr_codes()
└── forms.py
    ├── InvoiceForm
    ├── InvoiceItemForm
    ├── OfferForm
    ├── OfferItemForm
    └── PaymentForm
```

### 4. Templates App (Document Studio)
```
templates/
├── models.py
│   ├── DocumentTemplate
│   │   ├── Template details
│   │   ├── Header & footer
│   │   ├── Styling (colors, fonts)
│   │   ├── Logo
│   │   ├── Custom CSS
│   │   └── HTML template
│   └── TemplateVariable
│       ├── Variable definitions
│       └── Usage examples
├── views.py
│   ├── template_list()
│   ├── template_* (CRUD operations)
│   ├── template_preview()
│   └── template_studio()
└── forms.py
    └── DocumentTemplateForm
```

### 5. Subscriptions App (Stripe Integration)
```
subscriptions/
├── models.py
│   ├── Subscription
│   │   ├── Plan & status
│   │   ├── Stripe IDs
│   │   ├── Period dates
│   │   ├── Usage tracking
│   │   └── Limit checking
│   ├── SubscriptionHistory
│   │   └── Plan changes
│   └── Invoice (Stripe invoices)
│       └── Payment tracking
├── views.py
│   ├── subscription_plans()
│   ├── create_checkout_session()
│   ├── subscription_success()
│   ├── current_subscription()
│   ├── cancel_subscription()
│   └── stripe_webhook()
├── middleware.py
│   └── SubscriptionMiddleware
│       ├── Status checking
│       └── Limit enforcement
└── context_processors.py
    └── subscription_context()
        └── Global plan data
```

### 6. AI Assistant App (Gemini Integration)
```
ai_assistant/
├── models.py
│   ├── AIConversation
│   │   └── Chat threads
│   ├── AIMessage
│   │   ├── User messages
│   │   ├── AI responses
│   │   └── Context data
│   └── AISuggestion
│       ├── AI recommendations
│       ├── Related objects
│       └── Applied/dismissed status
├── services.py
│   └── GeminiAssistant
│       ├── chat()
│       ├── generate_email_draft()
│       ├── analyze_deal()
│       ├── suggest_tasks()
│       ├── generate_template_content()
│       └── smart_search()
└── views.py
    ├── ai_chat()
    ├── ai_suggestions()
    ├── generate_email()
    ├── analyze_deal_view()
    ├── suggest_tasks_view()
    ├── dismiss_suggestion()
    └── apply_suggestion()
```

## 🔄 Data Flow

### User Registration Flow
```
1. User fills registration form
2. Create User account
3. Create free Subscription
4. Login user
5. Redirect to dashboard
```

### Invoice Creation Flow
```
1. User creates invoice
2. Add line items
3. Calculate totals (subtotal, tax, total)
4. Add payment URL (optional)
5. Generate QR code (if payment URL exists)
6. Save invoice
7. Can send to client
```

### Payment Matching Flow
```
1. Payment received (manual or Stripe)
2. Try automatic matching:
   - Match by amount
   - Match by currency
   - Match by invoice status
3. If matched:
   - Update invoice paid_amount
   - Update invoice status
   - Mark payment as matched
4. If not matched:
   - Keep as unmatched
   - Try again in daily Celery task
```

### AI Chat Flow
```
1. User sends message
2. Check AI usage limits
3. Get conversation history
4. Get CRM context
5. Send to Gemini API
6. Receive AI response
7. Store message & response
8. Increment usage counter
9. Display to user
```

### Subscription Upgrade Flow
```
1. User selects plan
2. Create Stripe Checkout session
3. User pays in Stripe
4. Stripe sends webhook
5. Update subscription
6. Create history entry
7. Notify user
8. Redirect to dashboard
```

## 🗄️ Database Schema

### Core Relationships
```
User (1) ──→ (*) Contact
User (1) ──→ (*) Company
User (1) ──→ (*) Deal
User (1) ──→ (*) Task
User (1) ──→ (*) Invoice
User (1) ──→ (*) Offer
User (1) ──→ (1) Subscription

Contact (*) ──→ (1) Company
Deal (*) ──→ (1) Contact
Deal (*) ──→ (1) Company
Deal (*) ──→ (1) Pipeline
Deal (*) ──→ (1) Stage
Task (*) ──→ (1) Contact
Task (*) ──→ (1) Company
Task (*) ──→ (1) Deal

Invoice (*) ──→ (1) Contact
Invoice (*) ──→ (1) Company
Invoice (*) ──→ (1) DocumentTemplate
Invoice (1) ──→ (*) InvoiceItem
Invoice (1) ──→ (*) Payment

Pipeline (1) ──→ (*) Stage
Pipeline (1) ──→ (*) Deal

AIConversation (1) ──→ (*) AIMessage
```

## 🔐 Security Layers

```
┌────────────────────────────────────────────┐
│         1. Django Security                 │
│   - CSRF Protection                        │
│   - XSS Prevention                         │
│   - SQL Injection Protection               │
│   - Password Hashing                       │
└────────────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│      2. Authentication Layer               │
│   - Session Management                     │
│   - Login Required Decorators              │
│   - User Permissions                       │
└────────────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│    3. Subscription Middleware              │
│   - Plan Verification                      │
│   - Usage Limits                           │
│   - Feature Access                         │
└────────────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│      4. Data Isolation                     │
│   - Owner-based Queries                    │
│   - User Data Separation                   │
│   - Team Member Access                     │
└────────────────────────────────────────────┘
                    ▼
┌────────────────────────────────────────────┐
│    5. External API Security                │
│   - Stripe Webhook Verification            │
│   - API Key Management                     │
│   - Environment Variables                  │
└────────────────────────────────────────────┘
```

## 🚀 Deployment Architecture

### Production Setup
```
┌─────────────┐
│   Nginx     │ (Reverse Proxy, SSL)
└──────┬──────┘
       │
┌──────▼──────┐
│  Gunicorn   │ (WSGI Server)
└──────┬──────┘
       │
┌──────▼──────┐
│   Django    │ (Application)
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼───┐ ┌─▼───────┐
│ PG   │ │ Redis   │
│ SQL  │ │ (Cache/ │
│      │ │ Celery) │
└──────┘ └─────────┘
```

### Celery Workers
```
┌──────────────┐
│ Celery Beat  │ (Scheduler)
└──────┬───────┘
       │ schedules
       ▼
┌──────────────┐
│ Celery Worker│ (Task Executor)
└──────┬───────┘
       │ stores in
       ▼
┌──────────────┐
│    Redis     │ (Message Broker)
└──────────────┘
```

## 📊 Performance Optimization

### Database Queries
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many
- Pagination for large lists
- Indexed fields

### Caching Strategy
- Redis for session storage
- Celery result backend
- Template caching (production)
- Static file caching

### Background Tasks
- Payment matching (daily)
- Email sending (async)
- QR code generation (async)
- Report generation (async)

## 🌐 API Structure (Ready for Expansion)

```
/api/v1/
├── /contacts/
├── /companies/
├── /deals/
├── /tasks/
├── /invoices/
├── /offers/
└── /payments/
```

Django REST Framework is installed and ready for API development.

## 🔄 Internationalization (i18n)

```
User Request
     ↓
Detect Language (from user preference)
     ↓
Load Translation File (bg or en)
     ↓
Translate UI Text
     ↓
Format Dates/Numbers (locale-specific)
     ↓
Render Response
```

## 📱 Responsive Design

```
Mobile (< 768px)
  ├── Single column layout
  ├── Hamburger menu
  └── Touch-friendly buttons

Tablet (768px - 1024px)
  ├── Two column layout
  ├── Collapsed sidebar
  └── Optimized forms

Desktop (> 1024px)
  ├── Full layout
  ├── Expanded navigation
  └── All features visible
```

## 🔧 Technology Stack

### Backend
- Python 3.11
- Django 4.2.7
- Django REST Framework 3.14.0
- Celery 5.3.4
- PostgreSQL / SQLite

### Frontend
- Bootstrap 5.3.0
- Bootstrap Icons 1.11.1
- jQuery 3.7.1
- Custom CSS

### External Services
- Stripe API (Payments)
- Gemini AI API (Artificial Intelligence)
- Redis (Caching & Celery)

### Libraries
- Pillow (Image processing)
- QRCode (QR generation)
- ReportLab (PDF generation)
- python-dateutil (Date handling)

## 📈 Scalability Considerations

### Horizontal Scaling
- Stateless application design
- Session storage in Redis
- Static files on CDN
- Database connection pooling

### Vertical Scaling
- Optimized queries
- Database indexing
- Efficient algorithms
- Memory management

### Data Growth
- Pagination everywhere
- Archiving old data
- Database partitioning ready
- Efficient file storage

## 🔍 Monitoring Points

### Application Metrics
- Active users
- Subscription distribution
- API response times
- Error rates

### Business Metrics
- New registrations
- Subscription upgrades
- Churn rate
- Revenue

### System Metrics
- Database performance
- Celery queue length
- Memory usage
- CPU usage

---

This architecture is designed for:
- **Scalability**: Can grow from 1 to 10,000+ users
- **Maintainability**: Clean, modular code structure
- **Security**: Multiple layers of protection
- **Performance**: Optimized queries and caching
- **Reliability**: Background tasks and error handling

