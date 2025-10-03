# 📝 Changelog

## [1.0.1] - 2025-10-03 (Latest)

### 🤖 Changed - AI Model Upgrade
- **Updated Gemini model** from `gemini-2.0-flash-exp` to `gemini-2.5-flash-lite`
- **Reason:** Better cost-efficiency and lower latency
- **Benefits:**
  - ✅ More cost-effective for high-volume AI requests
  - ✅ Faster response times (optimized for low latency)
  - ✅ Same 1M token context window
  - ✅ Latest generation model (September 2025)
  - ✅ Better price-performance ratio
- **Reference:** [Gemini 2.5 Flash-Lite Documentation](https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-lite)

### 📝 Updated Documentation
- README.md - Updated AI section
- FEATURES.md - Updated AI model reference
- Created AI_MODEL_INFO.md - Detailed model documentation

---

## [1.0.0] - 2025-10-03 (Initial Release)

### ✨ Added - Complete CRM System

#### **Core Features:**
- ✅ User authentication and registration
- ✅ Contact management (CRUD)
- ✅ Company management (CRUD)
- ✅ Deal pipeline with stages
- ✅ Task management
- ✅ Activity logging

#### **Financial Features:**
- ✅ Invoice generation with line items
- ✅ Offer/quote system
- ✅ Payment tracking
- ✅ QR code generation for Stripe payments
- ✅ Automatic payment-to-invoice matching
- ✅ PDF export

#### **Template Studio:**
- ✅ Visual template editor
- ✅ Custom branding (logos, colors, fonts)
- ✅ Template preview
- ✅ Variable system
- ✅ Custom CSS/HTML support

#### **Subscription Management:**
- ✅ Multi-tier plans (Free, Basic €29, Pro €99, Enterprise €299)
- ✅ Stripe integration
- ✅ Webhook handling
- ✅ Usage tracking
- ✅ Automatic limit enforcement

#### **AI Features:**
- ✅ AI chat assistant (Gemini)
- ✅ Email generation
- ✅ Deal analysis
- ✅ Task suggestions
- ✅ Conversation history
- ✅ Usage limits per plan

#### **Internationalization:**
- ✅ Bulgarian language (primary) - 200+ strings translated
- ✅ English language (secondary)
- ✅ Language switcher in UI
- ✅ Compiled translations (.mo files)

#### **Infrastructure:**
- ✅ SQLite database (51 tables)
- ✅ Celery background tasks
- ✅ WhiteNoise static file serving
- ✅ Django admin panel
- ✅ Production-ready settings

#### **Documentation:**
- ✅ README.md - Complete setup guide
- ✅ QUICKSTART.md - 5-minute guide
- ✅ FEATURES.md - All features listed
- ✅ ARCHITECTURE.md - Technical details
- ✅ BULGARIAN_I18N_GUIDE.md - Language configuration
- ✅ TECH_STACK.md - Technology overview
- ✅ TESTING_GUIDE.md - Testing scenarios

#### **Templates:**
- ✅ 41 HTML templates created
- ✅ Bootstrap 5 responsive design
- ✅ Modern, professional UI
- ✅ Mobile-friendly layouts

---

## 🔮 Planned Features (Future)

### **v1.1 (Planned)**
- [ ] Email campaign management
- [ ] Advanced reporting dashboard
- [ ] Export data to CSV/Excel
- [ ] Calendar integration
- [ ] Kanban board for deals
- [ ] Mobile app (React Native)

### **v1.2 (Planned)**
- [ ] Zapier integration
- [ ] WhatsApp integration
- [ ] Advanced workflow automation
- [ ] Custom field types
- [ ] Team collaboration features
- [ ] Advanced analytics

### **v2.0 (Future)**
- [ ] Multi-tenancy support
- [ ] White-label capabilities
- [ ] Advanced API endpoints
- [ ] Marketplace for templates
- [ ] Third-party app integrations

---

## 🐛 Bug Fixes

### Version 1.0.1
- No bugs fixed (initial deployment working perfectly)

### Version 1.0.0
- All templates created (41 files)
- All migrations applied successfully
- Dependencies resolved (crispy-forms compatibility)

---

## 🔧 Technical Changes

### Version 1.0.1
- **AI Model:** gemini-2.0-flash-exp → gemini-2.5-flash-lite
- **Performance:** Improved response times
- **Cost:** Reduced AI processing costs

### Version 1.0.0
- **Framework:** Django 4.2.7
- **Database:** SQLite 3.x (production-ready for PostgreSQL)
- **Python:** 3.11+ support
- **Dependencies:** 17 core packages + 30+ sub-dependencies

---

## 📊 Statistics

### **Version 1.0.1:**
- Files Modified: 3
- New Documentation: 1 (AI_MODEL_INFO.md)
- Impact: All AI features (improved performance)

### **Version 1.0.0:**
- Total Files: 110+
- Python Files: 59
- HTML Templates: 41
- Documentation: 8 guides
- Translation Strings: 200+
- Database Tables: 51
- Features: 200+

---

## 🎯 Migration Notes

### **From 1.0.0 to 1.0.1:**
No database changes required. Simply restart the server:
```bash
pkill -f "manage.py runserver"
python manage.py runserver 8001
```

AI features will automatically use the new Flash-Lite model!

---

## 📚 Version History

| Version | Date | Description | Status |
|---------|------|-------------|--------|
| 1.0.1 | 2025-10-03 | AI model upgrade to Flash-Lite | ✅ Current |
| 1.0.0 | 2025-10-03 | Initial release - Full CRM | ✅ Stable |

---

## 🙏 Credits

**AI Models:**
- Gemini 2.5 Flash-Lite by Google
- Model documentation: https://ai.google.dev/

**Frameworks & Libraries:**
- Django by Django Software Foundation
- Bootstrap by Twitter
- Stripe API by Stripe, Inc.
- And 30+ open-source contributors

---

**Current Version:** 1.0.1  
**Release Date:** October 3, 2025  
**Status:** ✅ Production Ready  
**AI Model:** Gemini 2.5 Flash-Lite (Latest)

