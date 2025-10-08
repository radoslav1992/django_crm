# FAQ System Setup Guide

## Какво е създадено?

Пълна FAQ (Често задавани въпроси) система с:

- ✅ 7 категории въпроси
- ✅ 20+ FAQ въпроса на български и английски
- ✅ Подробни ръководства в Markdown формат
- ✅ Admin panel за управление
- ✅ Търсене и филтриране
- ✅ Markdown rendering за beautiful formatting
- ✅ Интеграция в footer на сайта

## Setup Instructions

### Стъпка 1: Migrations

```bash
python manage.py makemigrations faq
python manage.py migrate faq
```

### Стъпка 2: Load FAQ Data

```bash
python manage.py load_faq
```

Това ще създаде:
- 7 категории
- 20+ въпроса на български и английски
- Links към подробни ръководства

### Стъпка 3: Рестартирай сървъра

```bash
python manage.py runserver
```

### Стъпка 4: Посети FAQ

Отворете браузър на: `http://localhost:8000/bg/faq/`

## Създадени файлове

### Apps and Models:
```
apps/faq/
├── __init__.py
├── apps.py
├── models.py (FAQCategory, FAQItem)
├── admin.py (Admin interface)
├── views.py (faq_home, faq_category, faq_detail, faq_search)
├── urls.py
└── management/
    └── commands/
        └── load_faq.py (Initial data loader)
```

### Templates:
```
templates/faq/
├── faq_home.html (Main FAQ page with all categories)
├── faq_category.html (Category view with questions)
├── faq_detail.html (Question detail with markdown guide)
└── faq_search.html (Search results)
```

### Guides (Markdown):
```
apps/faq/guides/
├── stripe-payment-setup.md (Stripe setup guide)
├── resend-email-setup.md (Resend email guide)
├── invoice-management.md (Invoice & offer management)
├── crm-basics.md (CRM system guide)
└── ai-assistant.md (AI features guide)
```

## FAQ Categories

1. **Stripe плащания** - Payment setup and integration
2. **Имейл комуникация** - Resend setup and email templates
3. **Фактури и оферти** - Invoice and offer management
4. **CRM Система** - Contacts, deals, tasks
5. **AI Асистент** - AI features and automation
6. **Шаблони** - Template Studio
7. **Настройки и профил** - User settings

## Features

### ✅ Multi-language Support

- Questions stored in Bulgarian and English
- Auto-selects language based on user preference
- Fallback to Bulgarian if English not available

### ✅ Markdown Rendering

- Full markdown support in answers
- Code blocks with syntax highlighting
- Tables, lists, headers, images
- Beautiful formatting

### ✅ Search Functionality

- Search across all questions and answers
- Real-time search results
- Language-aware search

### ✅ View Tracking

- Counts how many times each question is viewed
- Popular questions highlighted
- Analytics for improving content

### ✅ Featured Questions

- Mark questions as featured
- Display on homepage for quick access
- Best practices and most important questions

### ✅ Admin Interface

- Easy content management
- WYSIWYG markdown editor
- Bulk operations
- Category ordering

## URLs

- **Homepage**: `/faq/` - All categories and featured questions
- **Category**: `/faq/category/<slug>/` - Questions in category
- **Question**: `/faq/question/<id>/` - Detailed answer with guide
- **Search**: `/faq/search/?q=query` - Search results

## Adding New Content

### Via Admin Panel:

1. Go to `/admin/faq/`
2. Add/Edit Categories or Questions
3. Write in Markdown format
4. Set featured questions
5. Activate/Deactivate content

### Via Code:

Create new markdown guide in `apps/faq/guides/`:

```markdown
# My New Guide

## Section 1

Content here...

## Section 2

More content...
```

Then create FAQ item linking to it:

```python
FAQItem.objects.create(
    category=category,
    question="My question?",
    answer="Short answer here",
    guide_file="my-new-guide.md"
)
```

## Markdown Examples

### Code Blocks:

\```python
def hello():
    print("Hello World")
\```

### Tables:

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

### Lists:

- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2

### Links:

[Link text](https://example.com)

### Images:

![Alt text](image-url.jpg)

## Customization

### Change Colors:

Edit `templates/faq/faq_home.html` CSS section.

### Add New Category:

```python
FAQCategory.objects.create(
    name="Нова категория",
    name_en="New Category",
    slug="new-category",
    description="Описание",
    icon="bi-star"  # Bootstrap icon
)
```

### Change Footer Links:

Edit `templates/base.html` footer section.

## Troubleshooting

### FAQ не се показва

**Check:**
1. Migrations applied: `python manage.py migrate faq`
2. Data loaded: `python manage.py load_faq`
3. Categories are active
4. URL is correct: `/faq/`

### Markdown не рендерира

**Check:**
1. `markdown` package installed: `pip install markdown`
2. Extensions loaded in views.py
3. CSS properly included

### Search не работи

**Check:**
1. Query parameter: `/faq/search/?q=query`
2. Questions contain searchable text
3. Language matches content

## Integration with Other Apps

### Link from CRM:

```django
<a href="{% url 'faq:home' %}">Help</a>
```

### Embed in email:

Include FAQ links in email templates:
```
Need help? Visit our FAQ: {{ site_url }}/faq/
```

### Widget in Dashboard:

Show popular questions in dashboard:
```python
featured = FAQItem.objects.filter(is_featured=True)[:5]
```

## Future Enhancements

Potential additions:

- 📹 Video tutorials
- 📊 Analytics dashboard
- 💬 Comments on questions
- 👍 Voting (helpful/not helpful)
- 🤖 AI-powered answers
- 📱 Mobile app view
- 📧 Email digest of new FAQs
- 🔗 Related questions suggestions

## Support

For questions about FAQ system:
- Check this guide
- Review code comments
- Contact development team

---

**FAQ System готова за използване!** 🎉

Access it at: `http://localhost:8000/bg/faq/`

