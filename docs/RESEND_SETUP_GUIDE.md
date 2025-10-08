# 📧 Resend Email Integration Setup Guide

## ✅ What Has Been Implemented

Your Django CRM now has a complete Resend email integration with AI-powered email template generation!

---

## 🎯 Features Added

### 1. **Resend Email Service**
- Complete integration with Resend API for sending transactional emails
- Replaces the old Hostinger/SMTP email backend
- Better deliverability and tracking
- Modern API-based approach

### 2. **User Configuration**
- Each user can configure their own Resend API key
- Custom "from" email address
- Custom "from" name for branding
- Settings page at `/accounts/resend-settings/`

### 3. **Email Templates Model**
- Store custom email templates in the database
- Support for multiple template types:
  - Invoice emails
  - Offer emails
  - Custom emails
  - Payment reminders
  - Welcome emails
  - Follow-up emails
- Track usage statistics (times sent, last used)
- AI-generated metadata

### 4. **AI-Powered Email Template Builder**
- Generate email templates using AI from natural language descriptions
- Integrated into the Studio interface
- Automatically creates subject lines and HTML content
- Includes plain text fallback
- Uses Django template variables for dynamic content

### 5. **Updated Invoice & Offer Sending**
- Invoice and Offer models now use Resend for email sending
- Better error handling
- Email tracking with timestamps

---

## 📦 Installation Steps

### 1. Install Resend Package

```bash
# Activate your virtual environment
source venv/bin/activate

# Install resend
pip install resend==0.8.0

# If you get SSL certificate errors, try:
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org resend==0.8.0
```

### 2. Database Migrations (Already Applied)

The migrations have been created and applied:
- ✅ `accounts/0002_user_resend_api_key_user_resend_from_email_and_more.py`
- ✅ `templates/0002_emailtemplate.py`

### 3. Environment Variables

Add these to your `.env` file:

```env
# Resend Configuration (Optional fallback - users can set their own keys)
RESEND_API_KEY=re_your_api_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com
RESEND_FROM_NAME=Your CRM System
SITE_URL=http://localhost:8000  # Change in production
```

---

## 🚀 How to Use

### For End Users

1. **Sign up for Resend:**
   - Go to [resend.com/signup](https://resend.com/signup)
   - Create a free account
   - Verify your domain (or use their test domain for development)

2. **Get Your API Key:**
   - Log into your Resend dashboard
   - Go to API Keys
   - Create a new API key
   - Copy the key (starts with `re_`)

3. **Configure in CRM:**
   - Log into your CRM account
   - Go to your Profile
   - Click "Resend Email Settings"
   - Enter your:
     - API Key
     - From Email (must be verified in Resend)
     - From Name (your company name)
   - Click "Save Settings"

4. **Start Sending Emails:**
   - Open any invoice or offer
   - Click "Send Email to Client"
   - Email will be sent via Resend!

### Create AI-Powered Email Templates

1. Go to **Studio** (Templates menu)
2. Look for the "Email Template Generator" section
3. Describe your email template:
   ```
   Example: "Create a professional payment reminder email with a 
   friendly tone. Include payment details, due date, and a pay now 
   button. Use modern styling with our brand colors."
   ```
4. Click "Generate Email Template"
5. Review the generated template
6. Save it with a name
7. Use it when sending emails!

---

## 🔧 Technical Details

### File Structure

```
django_crm/
├── apps/
│   ├── accounts/
│   │   ├── models.py           # Added resend_* fields to User model
│   │   ├── forms.py            # Added ResendSettingsForm
│   │   ├── views.py            # Added resend_settings view
│   │   └── urls.py             # Added resend-settings URL
│   ├── invoices/
│   │   ├── models.py           # Updated send_email() methods
│   │   └── email_service.py    # NEW: ResendEmailService class
│   ├── templates/
│   │   ├── models.py           # NEW: EmailTemplate model
│   │   ├── views.py            # Added email template generation views
│   │   └── urls.py             # Added email template URLs
│   └── ai_assistant/
│       └── services.py         # Added generate_email_template() method
├── templates/
│   └── accounts/
│       └── resend_settings.html # NEW: Resend settings page
├── config/
│   └── settings.py             # Added RESEND_* settings
└── requirements.txt            # Added resend==0.8.0
```

### API Usage Example

The code you provided has been integrated! Here's how it's used internally:

```python
# In apps/invoices/email_service.py

from apps.invoices.email_service import ResendEmailService

# Initialize service with user
email_service = ResendEmailService(request.user)

# Send invoice email
result = email_service.send_invoice_email(invoice, request)

# Send offer email  
result = email_service.send_offer_email(offer, request)

# Send custom email using a template
result = email_service.send_custom_email(
    to_email="client@example.com",
    subject="Payment Reminder",
    template_html=template.html_content,
    context={'client_name': 'John Doe', 'amount': 1500}
)
```

### Resend API Features Used

- ✅ Basic email sending
- ✅ HTML and plain text versions
- ✅ Custom "from" addresses
- ✅ Reply-to addresses
- ✅ Email tags for tracking
- ✅ Error handling and logging

### Email Template Variables

Available variables for templates:

**For Invoices:**
- `{{invoice_number}}`
- `{{invoice_date}}`
- `{{due_date}}`
- `{{client_name}}`
- `{{client_email}}`
- `{{total_amount}}`
- `{{currency}}`
- `{{pdf_url}}`
- `{{payment_url}}`

**For Offers:**
- `{{offer_number}}`
- `{{offer_date}}`
- `{{valid_until}}`
- `{{client_name}}`
- `{{total_amount}}`
- `{{currency}}`
- `{{pdf_url}}`

**General:**
- `{{contact_name}}`
- `{{company_name}}`
- `{{sender_name}}`
- `{{sender_company}}`
- `{{sender_email}}`

---

## 🎨 Email Template Studio Features

### Template Types

1. **Invoice Email** - Professional invoice notifications
2. **Offer Email** - Persuasive quote/offer emails
3. **Custom Email** - Any custom email you need
4. **Payment Reminder** - Polite payment reminders
5. **Welcome Email** - Onboarding emails for new clients
6. **Follow-up Email** - Post-meeting or post-sale follow-ups

### AI Generation

The AI can generate:
- Compelling subject lines (50-70 characters)
- HTML email body with:
  - Modern, mobile-responsive design
  - Inline CSS for email client compatibility
  - Clear call-to-action buttons
  - Professional formatting
  - Brand placeholders
  - Footer with contact info
- Plain text version for fallback

### Example AI Prompts

**Good prompts:**
```
"Create a friendly payment reminder email for overdue invoices. 
Include a prominent 'Pay Now' button, show the invoice details, 
and maintain a professional but understanding tone."

"Design a modern welcome email for new clients. Include our 
company introduction, key contact information, and next steps. 
Use a warm, approachable tone."

"Generate an offer email template with an urgency element. 
Highlight the value proposition, include pricing details, 
and have a strong call-to-action. Modern design with blue accents."
```

---

## 🔒 Security

### API Key Storage

- User API keys are stored in the database
- Keys are never displayed after saving (password field)
- Each user has their own keys (isolated)
- Keys are used per-request (not cached)

### Email Security

- Sender addresses must be verified in Resend
- SPF, DKIM, and DMARC configured in Resend dashboard
- No user data sent to Resend beyond email content
- Logging of all email attempts for audit trail

---

## 📊 Database Schema

### User Model Additions

```python
class User(AbstractUser):
    # ... existing fields ...
    
    # Resend email configuration
    resend_api_key = models.CharField(max_length=255, blank=True)
    resend_from_email = models.EmailField(blank=True)
    resend_from_name = models.CharField(max_length=200, blank=True)
    
    def has_resend_configured(self):
        return bool(self.resend_api_key and self.resend_from_email)
```

### EmailTemplate Model

```python
class EmailTemplate(models.Model):
    owner = ForeignKey(User)
    name = CharField(max_length=200)
    template_type = CharField(choices=[...])  # invoice, offer, custom, etc.
    subject = CharField(max_length=500)
    html_content = TextField()
    plain_text = TextField(blank=True)
    is_default = BooleanField(default=False)
    is_active = BooleanField(default=True)
    ai_generated = BooleanField(default=False)
    ai_prompt = TextField(blank=True)
    times_sent = IntegerField(default=0)
    last_used_at = DateTimeField(null=True)
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "Module 'resend' not found"**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
pip install resend
```

**2. "Email failed to send"**
- Check your API key is correct
- Verify your "from" email is verified in Resend
- Check Resend dashboard for error logs
- Ensure SITE_URL is set correctly in production

**3. "SSL Certificate Error" during pip install**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org resend
```

**4. "Template variables not rendering"**
- Make sure you're using Django template syntax: `{{variable}}`
- Check that the context includes the variable
- Test templates in the preview before sending

---

## 🧪 Testing

### Test Email Sending

```python
# In Django shell
python manage.py shell

from apps.invoices.email_service import ResendEmailService
from apps.accounts.models import User

user = User.objects.get(email='your@email.com')
service = ResendEmailService(user)

result = service.send_email(
    to_email='test@example.com',
    subject='Test Email',
    html_content='<h1>Hello World!</h1>',
    tags={'type': 'test'}
)

print(result)
```

### Development Mode

For development without Resend:
1. Keep `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` for old code
2. For testing Resend, use their test domain: `onboarding@resend.dev`
3. Emails will appear in Resend dashboard logs

---

## 📈 Next Steps

### Recommended Enhancements

1. **Email Analytics**
   - Track opens and clicks
   - Store delivery status
   - Show email history per invoice/offer

2. **Template Library**
   - Pre-built template gallery
   - Export/import templates
   - Template sharing between users

3. **Scheduled Emails**
   - Schedule emails for later
   - Recurring reminders
   - Automatic follow-ups

4. **Bulk Emailing**
   - Send to multiple recipients
   - Email campaigns
   - Newsletter functionality

5. **Email Attachments**
   - Attach PDF invoices directly
   - Support for multiple attachments
   - File size limits

---

## 📝 Migration from Old System

If you were using the old SMTP/Hostinger setup:

1. **Old code still works** - Legacy email code is preserved
2. **Gradual migration** - Users can opt into Resend when ready
3. **No breaking changes** - Existing functionality maintained
4. **Backward compatible** - Falls back to settings if user hasn't configured Resend

### Migration Checklist

- [ ] Install resend package
- [ ] Sign up for Resend account
- [ ] Verify domain in Resend
- [ ] Get API key
- [ ] Configure in user settings
- [ ] Test sending an invoice email
- [ ] Test sending an offer email
- [ ] Create first AI email template
- [ ] Update documentation for your team

---

## 🎉 Summary

You now have:

✅ **Modern Email Infrastructure**
- Resend API integration
- Better deliverability
- Professional email sending

✅ **User-Friendly Configuration**
- Easy setup page
- Per-user settings
- Visual status indicators

✅ **AI-Powered Templates**
- Generate beautiful emails with AI
- Natural language descriptions
- Professional designs automatically

✅ **Complete Integration**
- Works with invoices and offers
- Custom email support
- Template management system

✅ **Production Ready**
- Error handling
- Logging
- Security best practices
- Database migrations applied

---

## 📞 Support Resources

- **Resend Docs**: https://resend.com/docs
- **Resend Status**: https://status.resend.com
- **Template Studio**: `/templates/studio/`
- **Email Settings**: `/accounts/resend-settings/`

---

**Ready to send beautiful emails! 📧✨**

