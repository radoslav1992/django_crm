# 🔑 How to Update Your Gemini API Key

## ⚠️ Current Issue

Your `.env` file still contains the placeholder:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

This needs to be replaced with your **actual** Gemini API key.

---

## ✅ Solution - Update Your API Key

### **Option 1: Using Terminal (Recommended)**

Replace `YOUR_ACTUAL_KEY_HERE` with your real Gemini API key:

```bash
cd /Users/I567283/personal/django_crm

# Update the API key (replace with your real key!)
sed -i '' 's/GEMINI_API_KEY=.*/GEMINI_API_KEY=YOUR_ACTUAL_KEY_HERE/' .env

# Restart the server
pkill -f "manage.py runserver"
source venv/bin/activate
python manage.py runserver 8001
```

### **Option 2: Edit .env File Manually**

1. Open the `.env` file:
   ```bash
   nano .env
   ```

2. Find this line:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

3. Replace with your actual key:
   ```
   GEMINI_API_KEY=AIzaSyD-your-actual-key-here-without-quotes
   ```

4. Save: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

5. Restart server:
   ```bash
   pkill -f "manage.py runserver"
   source venv/bin/activate
   python manage.py runserver 8001
   ```

---

## 🔍 API Key Format

### **Correct Format:**
```env
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### **Common Mistakes:**
❌ `GEMINI_API_KEY="AIzaSy..."` (Don't use quotes)  
❌ `GEMINI_API_KEY= AIzaSy...` (No spaces after =)  
❌ `GEMINI_API_KEY=your-gemini-api-key-here` (Placeholder text)  

### **Valid Key Characteristics:**
- ✅ Starts with `AIzaSy`
- ✅ 39 characters long
- ✅ No quotes, no spaces
- ✅ Only alphanumeric characters and hyphens

---

## 🆓 How to Get Your Gemini API Key

1. **Visit:** https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click** "Create API Key"
4. **Copy** the key (starts with `AIzaSy`)
5. **Paste** into `.env` file

---

## 🧪 Verify It's Working

After updating the key:

1. **Test in Python:**
   ```bash
   cd /Users/I567283/personal/django_crm
   source venv/bin/activate
   python -c "
   from dotenv import load_dotenv
   import os
   load_dotenv()
   key = os.getenv('GEMINI_API_KEY')
   print(f'Key loaded: {key[:10]}...' if key and len(key) > 10 else 'Key not loaded!')
   print(f'Key length: {len(key) if key else 0}')
   print(f'Starts with AIzaSy: {key.startswith(\"AIzaSy\") if key else False}')
   "
   ```

   Should show:
   ```
   Key loaded: AIzaSyD...
   Key length: 39
   Starts with AIzaSy: True
   ```

2. **Test in Django:**
   Visit: http://localhost:8001/bg/ai/chat/
   Send a message
   Should get AI response!

---

## 🔐 Security Tips

- ✅ Never commit `.env` to git (already in .gitignore)
- ✅ Don't share your API key
- ✅ Keep it secret
- ✅ Rotate periodically
- ✅ Use different keys for dev/production

---

## 📝 Full .env Example

Your `.env` should look like this:

```env
SECRET_KEY=django-insecure-dev-key-change-in-production-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=sqlite:///db.sqlite3

STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

STRIPE_PRICE_FREE=price_free_plan
STRIPE_PRICE_BASIC=price_basic_monthly
STRIPE_PRICE_PRO=price_pro_monthly
STRIPE_PRICE_ENTERPRISE=price_enterprise_monthly

GEMINI_API_KEY=AIzaSyD-your-actual-39-character-key-here

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
REDIS_URL=redis://localhost:6379/0
LANGUAGE_CODE=bg
```

---

## 🚀 Quick Fix Command

Run this (replace with your actual key):

```bash
cd /Users/I567283/personal/django_crm
echo "GEMINI_API_KEY=AIzaSyD_PUT_YOUR_ACTUAL_KEY_HERE" >> .env.temp
grep -v "GEMINI_API_KEY" .env > .env.new
cat .env.temp >> .env.new
mv .env.new .env
rm .env.temp

# Restart server
pkill -f "manage.py runserver"
source venv/bin/activate
python manage.py runserver 8001
```

---

## ❓ Still Having Issues?

### **Check:**
1. Key is exactly 39 characters
2. Starts with `AIzaSy`
3. No spaces before or after the key
4. No quotes around the key
5. Server was restarted after updating

### **Test API Key Directly:**
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY" | head -20
```

If it returns model info, key is valid!

---

**Once you update the key, the AI features will work immediately!** 🤖

