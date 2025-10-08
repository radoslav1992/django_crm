# 🚀 Resend Quick Start Guide

## 30-Second Setup

### 1. Install Package
```bash
source venv/bin/activate
pip install resend
```

### 2. Add to .env
```env
RESEND_API_KEY=re_your_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com
RESEND_FROM_NAME=Your Company
SITE_URL=http://localhost:8000
```

### 3. Configure in UI
1. Go to `/accounts/resend-settings/`
2. Enter your Resend API key from [resend.com](https://resend.com)
3. Set your verified email address
4. Set your company name
5. Click "Save Settings"

### 4. Test It!
1. Open any invoice: `/invoices/1/`
2. Click "Send Email to Client"
3. Done! ✅

---

## 📧 Your Code Example (from Resend.com)

You wanted to use this code:

```python
import resend

resend.api_key = "••••••••••••••••••••••••••••••••••••"

r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": "dodnikov.radoslav@gmail.com",
  "subject": "Hello World",
  "html": "<p>Congrats on sending your <strong>first email</strong>!</p>"
})
```

**It's now integrated!** ✨

The system uses this internally in `apps/invoices/email_service.py`:

```python
# Your code is wrapped in ResendEmailService class
resend.api_key = user.resend_api_key  # Uses your API key

response = resend.Emails.send({
    "from": user.resend_from_email,     # Your verified email
    "to": invoice.client_email,          # Client's email
    "subject": f"Invoice {invoice.invoice_number}",
    "html": html_content,
    "tags": {"type": "invoice"}
})
```

---

## 🎨 AI Email Template Builder

### In the Studio

**URL**: `/templates/studio/`

**How to use:**

1. Click on "Email Template Builder" tab
2. Select template type (Invoice, Offer, Custom, etc.)
3. Describe what you want:
   ```
   "Create a professional payment reminder with a friendly 
   tone, payment details, and a blue 'Pay Now' button"
   ```
4. Click "Generate"
5. Review the template
6. Click "Save"
7. Done! Use it when sending emails

### Template Variables

Use these in your templates:

```django
{{client_name}}      - Client's name
{{invoice_number}}   - Invoice #
{{total_amount}}     - Amount
{{due_date}}         - Due date
{{payment_url}}      - Payment link
{{pdf_url}}          - PDF link
```

---

## 🔑 Get Your Resend API Key

1. Go to [resend.com/signup](https://resend.com/signup)
2. Create account (free tier available)
3. Verify your domain or use `onboarding@resend.dev` for testing
4. Go to **API Keys** in dashboard
5. Click **Create API Key**
6. Copy the key (starts with `re_`)
7. Paste in CRM settings at `/accounts/resend-settings/`

---

## ✅ What You Can Do Now

### Send Invoices & Offers
- ✅ Automated email sending
- ✅ Professional HTML templates
- ✅ PDF links included
- ✅ Payment links (if Stripe configured)
- ✅ Delivery tracking

### Create Custom Email Templates
- ✅ AI-generated templates
- ✅ Multiple template types
- ✅ Django template variables
- ✅ Reusable templates
- ✅ Usage statistics

### Studio Features
- ✅ Document templates (invoices/offers)
- ✅ Email templates (NEW!)
- ✅ AI generation for both
- ✅ Preview before saving
- ✅ Template management

---

## 🎯 Next Steps

1. **Install resend package** (if not done)
2. **Get API key** from resend.com
3. **Configure settings** at `/accounts/resend-settings/`
4. **Test sending** an invoice email
5. **Create email template** in Studio
6. **Send custom emails** to clients

---

## 🆘 Need Help?

- **Setup Guide**: See `RESEND_SETUP_GUIDE.md`
- **Resend Docs**: [resend.com/docs](https://resend.com/docs)
- **Settings Page**: `/accounts/resend-settings/`
- **Studio**: `/templates/studio/`
- **Your Profile**: `/accounts/profile/`

---

**That's it! You're ready to send beautiful emails with Resend! 🎉**

