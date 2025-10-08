# 🇧🇬 Bulgarian Language Configuration Guide

## ✅ Bulgarian as Primary Language - CONFIGURED!

The Django CRM system is fully configured with **Bulgarian (Български)** as the primary language and **English** as secondary.

---

## 📋 Configuration Details

### **Settings (config/settings.py)**
```python
LANGUAGE_CODE = 'bg'  # Bulgarian is default
TIME_ZONE = 'Europe/Sofia'  # Bulgarian timezone

LANGUAGES = [
    ('bg', 'Български'),  # Bulgarian - PRIMARY
    ('en', 'English'),     # English - SECONDARY
]
```

### **Translation Files**
- ✅ `locale/bg/LC_MESSAGES/django.po` - Bulgarian translations (200+ strings)
- ✅ `locale/bg/LC_MESSAGES/django.mo` - Compiled translations ← **ACTIVE**

---

## 🌐 How URLs Work with i18n

Django automatically prefixes URLs with language code:

| Language | URL Format | Example |
|----------|------------|---------|
| **Bulgarian** | `/bg/...` | `http://localhost:8001/bg/crm/` |
| **English** | `/en/...` | `http://localhost:8001/en/crm/` |
| **Auto-detect** | `/` | Redirects to `/bg/` or `/en/` |

When you visit `http://localhost:8001/`, Django:
1. Checks your browser language
2. Defaults to Bulgarian (`bg`) based on `LANGUAGE_CODE` setting
3. Redirects to `/bg/` or `/en/`

---

## 🎯 Language Switcher Added

### **Location 1: Main Navigation (for logged-in users)**
Added language switcher dropdown in navbar:
- 🇧🇬 Български
- 🇬🇧 English

### **Location 2: Landing Page (for visitors)**
Added language bar at the top of landing page

### **How to Use:**
1. Click the language dropdown
2. Select your preferred language
3. Page refreshes with new language
4. Language preference is saved in session

---

## 📝 Bulgarian Translation Coverage

### **Fully Translated Sections:**

#### **Navigation** (100% Bulgarian)
- Табло (Dashboard)
- Контакти (Contacts)
- Компании (Companies)
- Сделки (Deals)
- Задачи (Tasks)
- Фактури (Invoices)
- Студио за шаблони (Template Studio)
- AI Асистент (AI Assistant)

#### **Common Terms** (100% Bulgarian)
- Вход / Изход (Login/Logout)
- Регистрация (Register)
- Профил (Profile)
- Абонамент (Subscription)
- Търсене (Search)
- Създай (Create)
- Редактирай (Edit)
- Изтрий (Delete)
- Запази (Save)
- Отказ (Cancel)

#### **CRM Terms** (100% Bulgarian)
- Име (Name)
- Имейл (Email)
- Телефон (Phone)
- Адрес (Address)
- Компания (Company)
- Позиция (Position)
- Статус (Status)
- Активен/Неактивен (Active/Inactive)

#### **Financial Terms** (100% Bulgarian)
- Фактура (Invoice)
- Оферта (Offer)
- Плащане (Payment)
- Обща сума (Total)
- Данък (Tax)
- Падеж (Due Date)
- Платена (Paid)
- Просрочена (Overdue)

#### **Subscription Plans** (100% Bulgarian)
- Безплатен (Free)
- Базов (Basic)
- Професионален (Pro)
- Корпоративен (Enterprise)
- Надстрой сега (Upgrade Now)
- Текущ план (Current Plan)

---

## 🔧 How to Test Bulgarian Language

### **Option 1: Visit Bulgarian URL Directly**
```
http://localhost:8001/bg/
```

### **Option 2: Use Language Switcher**
1. Visit any page
2. Click language dropdown (🇧🇬 Български / 🇬🇧 English)
3. Select "🇧🇬 Български"

### **Option 3: Set Browser Language**
1. Set your browser to Bulgarian
2. Visit http://localhost:8001/
3. System auto-redirects to `/bg/`

---

## 📚 What Gets Translated

### **Automatically Translated:**
✅ All navigation menu items  
✅ Button labels  
✅ Form field labels  
✅ Status badges  
✅ Error messages  
✅ Success messages  
✅ Page titles  
✅ Table headers  
✅ Help text  
✅ Email templates  

### **NOT Translated (User Data):**
❌ Company names (entered by users)  
❌ Contact names (entered by users)  
❌ Custom field values (user data)  
❌ Notes and descriptions (user content)  

---

## 🎨 Visual Indicators

### **In Navigation:**
You'll see the language switcher showing:
- Current language: "Български" or "English"
- Flag emoji: 🇧🇬 or 🇬🇧
- Dropdown with both options

### **In URLs:**
- Bulgarian pages: `/bg/crm/`, `/bg/contacts/`, etc.
- English pages: `/en/crm/`, `/en/contacts/`, etc.

---

## ✅ Verification Checklist

Test Bulgarian translations work:

1. **Visit homepage:** http://localhost:8001/
   - Should redirect to `/bg/`
   - Landing page text in Bulgarian

2. **Login page:** http://localhost:8001/bg/login/
   - Form labels in Bulgarian
   - Buttons in Bulgarian

3. **Dashboard:** http://localhost:8001/bg/crm/
   - Navigation in Bulgarian
   - Statistics in Bulgarian

4. **Create forms:**
   - All field labels in Bulgarian
   - Validation messages in Bulgarian

5. **Switch language:**
   - Click "🇬🇧 English"
   - Everything switches to English
   - Click "🇧🇬 Български"
   - Everything switches back to Bulgarian

---

## 📖 Translation File Structure

### **Bulgarian Translation File:**
```
locale/bg/LC_MESSAGES/
├── django.po   (Source translations - editable)
└── django.mo   (Compiled translations - used by Django)
```

### **Sample Translations:**
```
msgid "Dashboard"
msgstr "Табло"

msgid "Contacts"
msgstr "Контакти"

msgid "Invoice"
msgstr "Фактура"

msgid "Create Account"
msgstr "Създай акаунт"
```

---

## 🔄 How to Add More Translations

### **1. Edit Translation File**
```bash
nano locale/bg/LC_MESSAGES/django.po
```

### **2. Add New Translations**
```
msgid "Your English Text"
msgstr "Вашият български текст"
```

### **3. Compile Translations**
```bash
python manage.py compilemessages
```

### **4. Restart Server**
The translations will be active immediately.

---

## 🌍 Default Language Behavior

### **When User First Visits:**
1. Django checks `LANGUAGE_CODE = 'bg'` in settings
2. Redirects to `/bg/` (Bulgarian)
3. All text displays in Bulgarian
4. User can switch to English if preferred

### **Language Persistence:**
- Language choice saved in session cookie
- Persists across page visits
- User can change anytime via dropdown

---

## 📱 Testing Scenarios

### **Scenario 1: New User (Bulgarian Default)**
```
1. Open http://localhost:8001/
2. See Bulgarian landing page
3. Register account in Bulgarian
4. Use CRM in Bulgarian
```

### **Scenario 2: English Preference**
```
1. Visit any page
2. Click language switcher
3. Select "🇬🇧 English"
4. All pages now in English
```

### **Scenario 3: Mixed Usage**
```
1. Some users prefer Bulgarian
2. Others prefer English
3. Each user chooses via dropdown
4. Preference saved per session
```

---

## 🎉 Current Status

✅ **Bulgarian** - Fully configured as PRIMARY  
✅ **English** - Available as SECONDARY  
✅ **Translations** - 200+ strings translated  
✅ **Compiled** - `.mo` file generated  
✅ **Active** - Working in application  
✅ **Switcher** - Added to navigation  
✅ **Default** - Bulgarian is default language  

---

## 📝 Quick Reference

### **Access Pages in Bulgarian:**
- Dashboard: `http://localhost:8001/bg/crm/`
- Contacts: `http://localhost:8001/bg/crm/contacts/`
- Companies: `http://localhost:8001/bg/crm/companies/`
- Invoices: `http://localhost:8001/bg/invoices/`

### **Access Pages in English:**
- Dashboard: `http://localhost:8001/en/crm/`
- Contacts: `http://localhost:8001/en/crm/contacts/`
- Companies: `http://localhost:8001/en/crm/companies/`
- Invoices: `http://localhost:8001/en/invoices/`

---

## 🚀 Your CRM Now Has:

✅ **Bulgarian Interface** - Primary language  
✅ **English Interface** - Secondary language  
✅ **Easy Switching** - Dropdown in navigation  
✅ **Auto-detection** - Based on browser/preference  
✅ **Session Persistence** - Remembers your choice  
✅ **Full Coverage** - All UI elements translated  

**Language Configuration: COMPLETE!** 🇧🇬 🇬🇧

Visit http://localhost:8001/bg/ to see the system in Bulgarian!

