from django.core.management.base import BaseCommand
from apps.faq.models import FAQCategory, FAQItem


class Command(BaseCommand):
    help = 'Load initial FAQ data into the database'

    def handle(self, *args, **options):
        self.stdout.write('Loading FAQ data...')

        # Create Categories
        categories_data = [
            {
                'name': 'Stripe плащания',
                'name_en': 'Stripe Payments',
                'slug': 'stripe-payments',
                'description': 'Как да настроя и използвам Stripe за онлайн плащания',
                'icon': 'bi-credit-card'
            },
            {
                'name': 'Имейл комуникация',
                'name_en': 'Email Communication',
                'slug': 'email-communication',
                'description': 'Настройка на Resend и изпращане на имейли',
                'icon': 'bi-envelope'
            },
            {
                'name': 'Фактури и оферти',
                'name_en': 'Invoices & Offers',
                'slug': 'invoices-offers',
                'description': 'Създаване и управление на фактури и оферти',
                'icon': 'bi-file-text'
            },
            {
                'name': 'CRM Система',
                'name_en': 'CRM System',
                'slug': 'crm-system',
                'description': 'Управление на контакти, компании и сделки',
                'icon': 'bi-people'
            },
            {
                'name': 'AI Асистент',
                'name_en': 'AI Assistant',
                'slug': 'ai-assistant',
                'description': 'Използване на изкуствен интелект за автоматизация',
                'icon': 'bi-robot'
            },
            {
                'name': 'Шаблони',
                'name_en': 'Templates',
                'slug': 'templates',
                'description': 'Създаване и персонализиране на шаблони',
                'icon': 'bi-palette'
            },
            {
                'name': 'Настройки и профил',
                'name_en': 'Settings & Profile',
                'slug': 'settings-profile',
                'description': 'Конфигуриране на системата и потребителски профил',
                'icon': 'bi-gear'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = FAQCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))

        # Create FAQ Items
        faq_items = [
            # Stripe Payments
            {
                'category': 'stripe-payments',
                'question': 'Как да създам Stripe линк за плащане?',
                'question_en': 'How to create a Stripe payment link?',
                'answer': 'Можете да създадете Stripe payment link директно от Stripe Dashboard или автоматично през CRM системата като настроите Stripe API ключовете си.',
                'answer_en': 'You can create a Stripe payment link directly from the Stripe Dashboard or automatically through the CRM system by configuring your Stripe API keys.',
                'guide_file': 'stripe-payment-setup.md',
                'is_featured': True
            },
            {
                'category': 'stripe-payments',
                'question': 'Как да добавя payment link към фактура?',
                'question_en': 'How to add payment link to invoice?',
                'answer': 'Редактирайте фактурата и въведете Stripe payment link в полето "Payment URL". При изпращане на имейл, клиентът ще получи бутон "Pay Now" който сочи към този линк.',
                'answer_en': 'Edit the invoice and enter the Stripe payment link in the "Payment URL" field. When sending an email, the client will receive a "Pay Now" button that points to this link.'
            },
            {
                'category': 'stripe-payments',
                'question': 'Какви тестови карти мога да използвам?',
                'question_en': 'What test cards can I use?',
                'answer': 'В test mode използвайте картата: **4242 4242 4242 4242** с всякакъв CVC (3 цифри) и бъдеща дата на изтичане.',
                'answer_en': 'In test mode use the card: **4242 4242 4242 4242** with any CVC (3 digits) and future expiration date.'
            },
            
            # Email Communication
            {
                'category': 'email-communication',
                'question': 'Как да настроя Resend за изпращане на имейли?',
                'question_en': 'How to setup Resend for sending emails?',
                'answer': 'Създайте Resend акаунт, добавете вашия домейн, генерирайте API ключ и го конфигурирайте в CRM системата през Settings → Resend Email Settings.',
                'answer_en': 'Create a Resend account, add your domain, generate an API key and configure it in the CRM system via Settings → Resend Email Settings.',
                'guide_file': 'resend-email-setup.md',
                'is_featured': True
            },
            {
                'category': 'email-communication',
                'question': 'Как AI генерира email шаблони?',
                'question_en': 'How does AI generate email templates?',
                'answer': 'Отидете в Template Studio → Email Templates, изберете тип (Invoice, Offer и др.), опишете какъв дизайн искате, и AI автоматично ще генерира HTML email с template variables и CTA бутони.',
                'answer_en': 'Go to Template Studio → Email Templates, select type (Invoice, Offer, etc.), describe what design you want, and AI will automatically generate HTML email with template variables and CTA buttons.'
            },
            {
                'category': 'email-communication',
                'question': 'Как да избера кой email template да използвам?',
                'question_en': 'How to select which email template to use?',
                'answer': 'При изпращане на фактура/оферта, системата ви показва форма за избор на template. Можете да изберете default template или някой от вашите custom AI генерирани templates.',
                'answer_en': 'When sending an invoice/offer, the system shows you a form to select a template. You can choose the default template or any of your custom AI-generated templates.'
            },
            
            # Invoices & Offers
            {
                'category': 'invoices-offers',
                'question': 'Как да създам фактура?',
                'question_en': 'How to create an invoice?',
                'answer': 'Отидете на Invoices → Create Invoice, попълнете информацията за клиента, добавете артикули, данъци се изчисляват автоматично. Можете директно да изпратите или да запазите като чернова.',
                'answer_en': 'Go to Invoices → Create Invoice, fill in client information, add line items, taxes are calculated automatically. You can send directly or save as draft.',
                'guide_file': 'invoice-management.md',
                'is_featured': True
            },
            {
                'category': 'invoices-offers',
                'question': 'Как да генерирам PDF на фактура?',
                'question_en': 'How to generate invoice PDF?',
                'answer': 'PDF се генерира автоматично при създаване на фактурата. Можете да го прегледате с "View PDF" или да го изтеглите с "Download PDF".',
                'answer_en': 'PDF is generated automatically when creating the invoice. You can preview it with "View PDF" or download it with "Download PDF".'
            },
            {
                'category': 'invoices-offers',
                'question': 'Какви статуси има фактурата?',
                'question_en': 'What statuses does an invoice have?',
                'answer': 'Фактурата може да бъде: Draft (чернова), Sent (изпратена), Partially Paid (частично платена), Paid (платена), Overdue (просрочена) или Cancelled (анулирана).',
                'answer_en': 'Invoice can be: Draft, Sent, Partially Paid, Paid, Overdue or Cancelled.'
            },
            
            # CRM System
            {
                'category': 'crm-system',
                'question': 'Как да добавя контакт в CRM?',
                'question_en': 'How to add a contact to CRM?',
                'answer': 'Отидете на CRM → Contacts → Create Contact, попълнете име, имейл, телефон и други данни. Можете също да импортирате контакти от CSV файл.',
                'answer_en': 'Go to CRM → Contacts → Create Contact, fill in name, email, phone and other data. You can also import contacts from CSV file.',
                'guide_file': 'crm-basics.md'
            },
            {
                'category': 'crm-system',
                'question': 'Как работи Pipeline Management?',
                'question_en': 'How does Pipeline Management work?',
                'answer': 'Pipeline показва сделките ви визуално по стадии: Lead, Qualified, Proposal, Negotiation, Closed. Можете да плъзгате (drag & drop) сделки между стадиите.',
                'answer_en': 'Pipeline shows your deals visually by stages: Lead, Qualified, Proposal, Negotiation, Closed. You can drag & drop deals between stages.'
            },
            {
                'category': 'crm-system',
                'question': 'Как да създам задача?',
                'question_en': 'How to create a task?',
                'answer': 'Отидете на CRM → Tasks → Create Task, въведете заглавие, описание, краен срок и priority. Можете да свържете задачата с контакт или сделка.',
                'answer_en': 'Go to CRM → Tasks → Create Task, enter title, description, deadline and priority. You can link the task to a contact or deal.'
            },
            
            # AI Assistant
            {
                'category': 'ai-assistant',
                'question': 'Как да настроя AI Асистента?',
                'question_en': 'How to setup AI Assistant?',
                'answer': 'Получете Gemini API key от Google AI Studio (makersuite.google.com/app/apikey), добавете го в .env файла като GEMINI_API_KEY или въведете в Settings → AI Configuration.',
                'answer_en': 'Get a Gemini API key from Google AI Studio (makersuite.google.com/app/apikey), add it to .env file as GEMINI_API_KEY or enter in Settings → AI Configuration.',
                'guide_file': 'ai-assistant.md',
                'is_featured': True
            },
            {
                'category': 'ai-assistant',
                'question': 'Какво може да прави AI?',
                'question_en': 'What can AI do?',
                'answer': 'AI може да генерира email и document шаблони, да създава task lists, да пише текстово съдържание, да дава business insights и да помага с автоматизация на процеси.',
                'answer_en': 'AI can generate email and document templates, create task lists, write text content, provide business insights and help with process automation.'
            },
            
            # Templates
            {
                'category': 'templates',
                'question': 'Какво е Template Studio?',
                'question_en': 'What is Template Studio?',
                'answer': 'Template Studio е инструмент за създаване на персонализирани шаблони за document (Invoice/Offer PDF) и email. Включва AI генератор за автоматично създаване на beautiful templates.',
                'answer_en': 'Template Studio is a tool for creating custom templates for documents (Invoice/Offer PDF) and emails. It includes an AI generator for automatically creating beautiful templates.'
            },
            {
                'category': 'templates',
                'question': 'Какви променливи мога да използвам в шаблоните?',
                'question_en': 'What variables can I use in templates?',
                'answer': 'Можете да използвате: {{client_name}}, {{invoice_number}}, {{total_amount}}, {{payment_url}}, {{pdf_url}}, {{sender_name}} и много други. Пълен списък има в Template Studio.',
                'answer_en': 'You can use: {{client_name}}, {{invoice_number}}, {{total_amount}}, {{payment_url}}, {{pdf_url}}, {{sender_name}} and many more. Full list is available in Template Studio.'
            },
            
            # Settings & Profile
            {
                'category': 'settings-profile',
                'question': 'Как да променя настройките на профила си?',
                'question_en': 'How to change my profile settings?',
                'answer': 'Кликнете на вашето име в горния десен ъгъл → Settings. Можете да промените име, имейл, парола, език и други настройки.',
                'answer_en': 'Click on your name in the top right corner → Settings. You can change name, email, password, language and other settings.'
            },
            {
                'category': 'settings-profile',
                'question': 'Как да сменя езика на системата?',
                'question_en': 'How to change system language?',
                'answer': 'Отидете в Settings → Language Settings, изберете Bulgarian или English и запазете. Системата автоматично ще смени езика.',
                'answer_en': 'Go to Settings → Language Settings, select Bulgarian or English and save. The system will automatically change the language.'
            },
        ]

        for item_data in faq_items:
            category_slug = item_data.pop('category')
            item_data['category'] = categories[category_slug]
            
            FAQItem.objects.get_or_create(
                question=item_data['question'],
                category=item_data['category'],
                defaults=item_data
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(faq_items)} FAQ items!'))
        self.stdout.write(self.style.SUCCESS('Done!'))

