# AI Асистент - Как да използвам изкуствения интелект

## Какво е AI Асистентът?

AI Асистентът е вграден изкуствен интелект (Google Gemini), който ви помага да:

- Генерирате съдържание за фактури и оферти
- Създавате email шаблони автоматично
- Генерирате task lists от описания
- Получавате бизнес insights
- Автоматизирате рутинни задачи

## Настройка на AI Асистента

### Стъпка 1: Получаване на Gemini API Key

1. Отидете на [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Влезте с Google акаунт
3. Кликнете **"Create API Key"**
4. Копирайте генерирания ключ

### Стъпка 2: Конфигуриране в CRM

**Метод A: През Environment Variables**
```bash
# Добавете в .env файла
GEMINI_API_KEY=AIzaSyD...
```

**Метод B: През Admin Panel**
1. Влезте като администратор
2. Отидете на **"Settings"** → **"AI Configuration"**
3. Въведете API ключа
4. Запазете

## Използване на AI Асистента

### AI Dashboard

1. Отидете на **"AI Assistant"** от главното меню
2. Ще видите dashboard с опции:
   - **Generate Content**: Генериране на текст
   - **Create Email Template**: Създаване на email шаблони
   - **Task Generator**: Генериране на задачи
   - **Business Insights**: Анализ и препоръки

## Генериране на Email Шаблони

### Стъпка по стъпка:

1. Отидете на **"Template Studio"** → **"Email Templates"**
2. Кликнете **"Generate with AI"**
3. Попълнете:

**Избор на тип:**
- Invoice Email
- Offer Email
- Payment Reminder
- Welcome Email
- Follow-up Email
- Custom

**AI Prompt (примери):**

Задача | Prompt
-------|-------
Професионален стил | "Професионален имейл за фактура с модерен дизайн и payment button"
Приятелски тон | "Приятелски имейл за оферта, с персонален тон и CTA бутон"
С графики | "Email с визуален дизайн, включващ таблица с цени и highlights"
Минималистичен | "Минималистичен email дизайн, clean и professional"

4. Кликнете **"Generate"**

### AI генерира автоматично:

- ✅ **Subject Line**: Оптимизирана заглавна линия
- ✅ **HTML Content**: Красив responsive HTML дизайн
- ✅ **Plain Text**: Text версия за email клиенти
- ✅ **Template Variables**: Автоматично вградени променливи
- ✅ **CTA Buttons**: Call-to-action бутони с реални URLs

### Preview & Edit:

1. Прегледайте генерирания шаблон
2. Редактирайте ако е необходимо
3. Запазете шаблона
4. Използвайте при изпращане на фактури

## Генериране на Document Шаблони

### За Invoice/Offer PDF:

1. Отидете на **"Template Studio"** → **"Document Templates"**
2. Кликнете **"Generate with AI"**
3. Опишете какво искате:

**Примерни prompts:**
```
"Модерен invoice шаблон с blue accent colors и минималистичен дизайн"

"Професионален offer template със large header и company logo section"

"Elegant invoice design with gradient background и modern typography"
```

4. AI генерира пълен HTML/CSS шаблон
5. Preview в реално време
6. Запазете и използвайте

## Task Generation (Генериране на задачи)

### Автоматично създаване на task lists:

1. Отидете на **"AI Assistant"** → **"Task Generator"**
2. Опишете вашата цел:

**Примери:**

```
"Трябва да подготвя оферта за нов клиент"

AI генерира:
□ Събери информация за клиента
□ Направи market research
□ Подготви ценова оферта
□ Създай offer document
□ Прегледай и редактирай
□ Изпрати на клиента
□ Насрочи follow-up call след 3 дни
```

```
"Искам да started email marketing campaign"

AI генерира:
□ Дефинирай target audience
□ Създай email list
□ Design email template
□ Напиши email content
□ Setup email automation
□ A/B test subject lines
□ Анализирай резултатите
```

3. AI автоматично създава задачи в CRM
4. Настройва deadlines
5. Приоритизира задачите

## Business Insights

### AI анализ на вашите данни:

1. Отидете на **"AI Assistant"** → **"Insights"**
2. AI анализира:
   - Sales trends
   - Customer behavior
   - Pipeline health
   - Revenue forecasts

### Примерни insights:

```
💡 "Сделките ви в стадий 'Proposal' остават средно 15 дни. 
   Препоръчваме по-агресивен follow-up след 7 дни."

💡 "Клиентите от технологичния сектор имат 23% по-висок 
   conversion rate. Фокусирайте се повече там."

💡 "Прогноза: Ако запазите текущия темп, ще достигнете 
   85% от месечната цел."
```

## Content Generation (Генериране на текст)

### Email съдържание:

```
Prompt: "Напиши follow-up email за клиент който не е отговорил 
        на оферта от миналата седмица"

AI генерира:
Subject: Имате ли въпроси относно нашата оферта?

Здравейте [Име],

Искам да се свържа с вас относно офертата която изпратих 
миналата седмица...
```

### Proposal text:

```
Prompt: "Напиши въведение за бизнес proposal за уеб дизайн услуги"

AI генерира професионален proposal text с:
- Company overview
- Services offered
- Value proposition
- Call to action
```

### Social media posts:

```
Prompt: "Създай LinkedIn post за нова функция в CRM системата"

AI генерира engaging post с hashtags.
```

## Advanced AI Features

### Smart Suggestions

AI автоматично предлага:

- **Best time to contact**: Оптимално време за контакт с клиент
- **Email subject lines**: A/B варианти за по-добър open rate
- **Deal insights**: Кои сделки трябва да приоритизирате
- **Follow-up reminders**: Кога да направите follow-up

### Natural Language Queries

Задавайте въпроси на естествен език:

```
"Покажи ми всички сделки над 10,000 EUR в стадий Negotiation"
"Кои клиенти не съм контактувал от месец?"
"Създай report за продажбите през Q1"
```

AI разбира и изпълнява!

### Automated Workflows

Създавайте AI-powered workflows:

1. **Trigger**: Нов Lead
2. **AI Action**: Генерира персонализиран welcome email
3. **AI Action**: Създава onboarding tasks
4. **AI Action**: Насрочва follow-up
5. **Result**: Автоматизиран процес!

## Template Variables

Когато AI генерира шаблони, автоматично използва променливи:

### Invoice Variables:
- `{{invoice_number}}`
- `{{client_name}}`
- `{{total_amount}}`
- `{{due_date}}`
- `{{payment_url}}`
- `{{pdf_url}}`

### Contact Variables:
- `{{contact_name}}`
- `{{company_name}}`
- `{{email}}`
- `{{phone}}`

### Custom Variables:
Можете да дефинирате собствени променливи.

## AI Quality Tips

### За най-добри резултати:

1. **Бъдете конкретни**: 
   ❌ "Направи email"
   ✅ "Създай професионален invoice email с modern design, blue color scheme и prominent payment button"

2. **Дайте контекст**:
   ❌ "Генерирай задачи"
   ✅ "Генерирай задачи за затваряне на B2B SaaS deal с Enterprise клиент, включително demo, proposal, legal review"

3. **Уточнете стила**:
   - "Formal professional tone"
   - "Friendly casual style"
   - "Technical and detailed"
   - "Brief and concise"

4. **Итерирайте**:
   Ако резултатът не е точно какво искате, рефинирайте prompt-а.

## Pricing & Limits

### Gemini API Limits:

- **Free tier**: 60 requests/minute
- **Paid tier**: Higher limits

### CRM Usage:

- AI генерира съдържание on-demand
- Няма допълнителна такса от CRM
- Плащате само за Gemini API usage

### Rate Limiting:

Ако достигнете лимита:
- Изчакайте 1 минута
- Upgrade Gemini plan
- Използвайте batch generation

## Privacy & Security

### Вашите данни:

- ❌ AI **НЕ** съхранява вашите данни
- ✅ Requests са **temporary**
- ✅ Template съдържание е **местно**
- ✅ **Encryption** при комуникация с API

### Best Practices:

- Не включвайте sensitive data в prompts
- Прегледайте AI генерирано съдържание преди изпращане
- Използвайте test mode за тестване

## Troubleshooting

### Problem: "AI generation failed"

**Решения:**
- Проверете API key
- Проверете internet connection
- Опитайте с по-прост prompt
- Проверете Gemini API status

### Problem: "Low quality output"

**Решения:**
- Подобрете prompt-а с повече детайли
- Дайте примери за желания стил
- Използвайте по-новия Gemini модел

### Problem: "Rate limit exceeded"

**Решения:**
- Изчакайте 1 минута
- Разпределете requests във времето
- Upgrade API plan

## Examples Gallery

### Email Templates:

Вижте примери на AI генерирани шаблони в галерията.

### Task Lists:

Browse популярни AI генерирани task templates.

### Prompts Library:

Готови prompts за различни случаи.

## Tips & Tricks

1. **Reuse successful prompts**: Запазете работещи prompts
2. **Combine features**: Използвайте AI + Custom edits
3. **A/B test**: Генерирайте варианти и тествайте
4. **Learn from examples**: Проучете Gallery
5. **Iterate quickly**: AI генерира бързо, експериментирайте

## Future AI Features

Очаквайте скоро:

- 🔮 Predictive analytics
- 🤖 AI Sales Coach
- 📊 Advanced reporting
- 🎯 Lead scoring
- 🔄 Workflow automation

---

**Използвайте AI и спестете време!** 🤖✨

