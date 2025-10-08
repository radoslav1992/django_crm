# Email Functionality Guide

## ✅ Implemented Features

### 📧 **Invoice & Offer Email Sending**

Your Django CRM now has complete email functionality for invoices and offers!

---

## 🎯 What Was Added

### 1. **Email Tracking Fields**
Both Invoice and Offer models now track:
- `email_sent` - Whether the email has been sent
- `email_sent_at` - Timestamp of when the email was sent

### 2. **Email Sending Methods**
- `invoice.send_email(request)` - Sends invoice email to client
- `offer.send_email(request)` - Sends offer email to client

### 3. **Email Templates**
Beautiful HTML email templates:
- `templates/invoices/email_invoice.html` - Invoice email template
- `templates/invoices/email_offer.html` - Offer email template

Both templates include:
- Professional design with your branding
- Document details (number, date, total amount)
- Link to view/download PDF
- Payment link button (for invoices with Stripe payment URL)
- Responsive design

### 4. **UI Integration**
- **Send Email Button** on invoice and offer detail pages
- **Email Status Badge** showing when email was sent
- **Disabled state** if client email is missing
- **Confirmation dialog** before sending

---

## 📖 How to Use

### **Sending an Invoice Email**

1. Go to any invoice detail page
2. Ensure the invoice has a client email address
3. Click the green **"Send Email to Client"** button
4. Confirm the action
5. Email is sent automatically!

**What happens:**
- Email is sent to `client_email`
- Status changes from "Draft" to "Sent" (if applicable)
- Email tracking fields are updated
- Success message is displayed

### **Sending an Offer Email**

Same process as invoices - just go to an offer detail page!

---

## ⚙️ Email Configuration

### **Current Setup**

Your email settings in `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # For development
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### **For Development (Current)**

Emails are printed to the console - you can see them in the terminal where your Django server is running.

### **For Production**

Change `EMAIL_BACKEND` to:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

### **Recommended Email Providers**

1. **SendGrid** (Recommended for production)
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=your-sendgrid-api-key
   DEFAULT_FROM_EMAIL=noreply@yourdomain.com
   ```

2. **Mailgun**
   ```env
   EMAIL_HOST=smtp.mailgun.org
   EMAIL_PORT=587
   EMAIL_HOST_USER=postmaster@yourdomain.com
   EMAIL_HOST_PASSWORD=your-mailgun-password
   ```

3. **AWS SES**
   ```env
   EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-ses-smtp-username
   EMAIL_HOST_PASSWORD=your-ses-smtp-password
   ```

---

## 🔍 Technical Details

### **Email Content**

Each email includes:
- **Subject**: "Invoice #INV-001" or "Offer #OFF-001"
- **HTML version**: Beautiful, responsive design
- **Plain text fallback**: For email clients that don't support HTML
- **PDF link**: Direct link to view/download the document
- **Reply-to**: Set to the invoice/offer owner's email

### **Automatic Status Updates**

When an email is sent:
- If status is "Draft" → automatically changes to "Sent"
- `email_sent` flag is set to `True`
- `email_sent_at` is set to current timestamp

### **Error Handling**

The system handles:
- ❌ Missing client email - shows disabled button
- ❌ SMTP errors - displays error message to user
- ❌ Network issues - graceful failure with feedback

---

## 🚀 Future Enhancements

Consider adding:
1. **Automatic Email Sending** - Send email automatically when invoice is created
2. **Email Templates Editor** - Allow users to customize email templates
3. **Email Tracking** - Track opens, clicks, and replies
4. **Bulk Email Sending** - Send multiple invoices at once
5. **Email Scheduling** - Schedule emails for later
6. **CC/BCC Options** - Add additional recipients
7. **Attachment Support** - Attach PDF directly to email
8. **Email History** - Track all sent emails for an invoice

---

## 📝 Migration Applied

Database migration `0002_add_email_tracking` has been applied successfully.

If you're deploying to production, make sure to run:
```bash
python manage.py migrate invoices
```

---

## 🧪 Testing

### Test in Development:
1. Create or edit an invoice
2. Add a client email
3. Click "Send Email to Client"
4. Check your terminal - you'll see the email content printed
5. Verify the email status badge appears

### Test in Production:
1. Configure proper SMTP settings
2. Add a real email address
3. Send test email to yourself
4. Verify email is received and looks good

---

## 📊 URLs Added

- `/invoices/<id>/send-email/` - Send invoice email
- `/invoices/offers/<id>/send-email/` - Send offer email

---

## ✨ UI Improvements

### Invoice/Offer Detail Pages Now Show:
- ✅ Green "Send Email to Client" button
- ✅ "Email Sent" badge with timestamp
- ✅ Disabled state if no email address
- ✅ Confirmation dialog before sending

---

Enjoy your new email functionality! 📧🎉

