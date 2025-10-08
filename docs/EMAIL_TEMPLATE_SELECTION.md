# Email Template Selection Feature

## ✨ What Was Added

The system now asks you to **choose which email template to use** before sending invoices/offers!

## 🎯 How It Works

### 1. **Click "Send Email to Client"**
   - On any invoice or offer detail page
   - Instead of sending immediately, you'll see a template selection form

### 2. **Choose Your Template**
   - **Default Template**: Standard professional email
   - **Custom Templates**: Your AI-generated or manually created templates
   - Preview shows the subject line before sending

### 3. **Send!**
   - Click "Send Email" button
   - Email is sent with your selected template
   - Template usage is tracked automatically

---

## 📋 Template Selection Flow

```
Invoice/Offer Detail Page
    ↓
Click "Send Email to Client" (GET request)
    ↓
Template Selection Form appears
    ↓
Select template (or use default)
    ↓
Click "Send Email" (POST request)
    ↓
Email sent with chosen template ✅
```

---

## 🎨 Create Custom Templates

### In Template Studio:

1. Go to `/templates/studio/`
2. Click **"Email Templates"** tab
3. Choose template type: Invoice, Offer, Custom, etc.
4. Enter AI prompt or design manually
5. Save template
6. Set as default (optional)

### Template Variables Available:

```django
{{contact_name}} / {{client_name}}
{{contact_email}} / {{client_email}}
{{company_name}}
{{invoice_number}} / {{offer_number}}
{{invoice_date}} / {{offer_date}}
{{due_date}} / {{valid_until}}
{{total_amount}}
{{currency}}
{{payment_url}}
{{pdf_url}}
{{sender_name}}
{{sender_company}}
{{sender_email}}
```

---

## 🔧 Technical Changes

### Files Modified:

1. **`apps/invoices/views.py`**
   - `invoice_send_email`: GET shows form, POST sends
   - `offer_send_email`: GET shows form, POST sends

2. **`apps/invoices/models.py`**
   - `Invoice.send_email()`: Accepts `email_template_id`
   - `Offer.send_email()`: Accepts `email_template_id`

3. **`apps/invoices/email_service.py`**
   - `send_invoice_email()`: Uses custom template if provided
   - `send_offer_email()`: Uses custom template if provided
   - Tracks template usage with `increment_usage()`

4. **`templates/invoices/send_email_form.html`** ✨ NEW
   - Beautiful template selection UI
   - Shows available templates
   - Preview functionality
   - Link to Template Studio

5. **`templates/invoices/invoice_detail.html`**
   - Removed confirmation dialog (form replaces it)

6. **`templates/invoices/offer_detail.html`**
   - Removed confirmation dialog (form replaces it)

---

## 💡 Features

✅ **Smart Default**: Default templates are pre-selected  
✅ **AI Badge**: Shows which templates are AI-generated  
✅ **Preview**: See subject line before sending  
✅ **Usage Tracking**: Tracks how many times each template is used  
✅ **Fallback**: Always works even with no custom templates  
✅ **Links**: Direct link to Template Studio to create new templates

---

## 🚀 Testing

1. **Create a test invoice/offer** with client email
2. **Click "Send Email to Client"**
3. **You should see**: Template selection form
4. **Select a template** (or use default)
5. **Click "Send Email"**
6. **Email is sent!** ✅

---

## 📊 Template Usage

Each time a template is used:
- `times_sent` counter increases
- `last_used_at` timestamp updates
- Helps you see which templates work best!

View usage stats in Template Studio → Email Templates list.

---

## 🎉 Benefits

✅ **Flexibility**: Choose the right template for each client  
✅ **Personalization**: Different emails for different situations  
✅ **Testing**: A/B test different email styles  
✅ **Branding**: Maintain consistent branding across emails  
✅ **AI Power**: Generate professional templates instantly

---

## 🔗 Related Features

- **Template Studio**: `/templates/studio/`
- **Email Templates List**: `/templates/email/`
- **AI Generation**: Built-in with Gemini
- **Resend Integration**: Reliable email delivery
- **SSL Fix**: Works on macOS out of the box

---

**Ready to use!** 🎊

Just restart your server and try sending an invoice/offer email!

