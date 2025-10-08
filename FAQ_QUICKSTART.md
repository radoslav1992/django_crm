# FAQ System - Quick Start 🚀

## Стъпка 1: Migrations

```bash
python manage.py makemigrations faq
python manage.py migrate faq
```

## Стъпка 2: Load Data

```bash
python manage.py load_faq
```

Това създава:
- ✅ 7 категории на български
- ✅ 20+ въпроса (BG + EN)
- ✅ Линкове към ръководства

## Стъпка 3: Restart & Visit

```bash
python manage.py runserver
```

Отворете: **http://localhost:8000/bg/faq/**

---

## 📋 Какво има вътре?

### Категории:
1. **Stripe плащания** 💳
2. **Имейл комуникация** ✉️
3. **Фактури и оферти** 📄
4. **CRM Система** 👥
5. **AI Асистент** 🤖
6. **Шаблони** 🎨
7. **Настройки** ⚙️

### Featured Guides:
- ✅ **Stripe Payment Setup** (как да създам payment link)
- ✅ **Resend Email Setup** (как да настроя Resend)
- ✅ **Invoice Management** (как да създам и изпратя фактури)
- ✅ **CRM Basics** (как да използвам CRM)
- ✅ **AI Assistant** (как да използвам AI)

---

## 🔗 Къде да намеря FAQ?

- **Footer link**: На всяка страница (долу)
- **Direct URL**: `/faq/`
- **Search**: `/faq/search/?q=query`

---

## ✏️ Как да редактирам?

### През Admin:

```
http://localhost:8000/admin/faq/
```

### През файлове:

```
apps/faq/guides/
├── stripe-payment-setup.md
├── resend-email-setup.md
├── invoice-management.md
├── crm-basics.md
└── ai-assistant.md
```

Всички guides са **Markdown** - лесно се редактират!

---

## 📚 Документация

Пълна документация:
- `docs/FAQ_SYSTEM_SUMMARY.md` - Пълен summary
- `docs/FAQ_SETUP_GUIDE.md` - Setup guide

---

**Готово! FAQ системата работи! 🎉**

