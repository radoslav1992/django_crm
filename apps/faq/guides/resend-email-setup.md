# Настройка на Resend за изпращане на имейли

## Какво е Resend?

Resend е модерна платформа за изпращане на имейли, която ви позволява да изпращате транзакционни имейли (фактури, оферти, известия) с висока надеждност и доставяемост.

## Стъпка 1: Създаване на Resend акаунт

1. Отидете на [resend.com](https://resend.com)
2. Кликнете **"Sign Up"** (Регистрация)
3. Регистрирайте се с имейл или GitHub
4. Потвърдете акаунта си

## Стъпка 2: Добавяне на домейн

### Защо е нужен собствен домейн?

За професионално изпращане на имейли е препоръчително да използвате собствения си домейн (example@yourdomain.com) вместо @resend.dev.

### Добавяне на домейн:

1. В Resend Dashboard отидете на **"Domains"**
2. Кликнете **"Add Domain"**
3. Въведете домейна си (например: `yourdomain.com`)
4. Resend ще ви даде DNS записи за добавяне

### DNS Конфигурация:

Добавете следните записи в DNS настройките на домейна си:

```
TXT Record:
Host: @ или yourdomain.com
Value: v=DKIM1; k=rsa; p=MIGfMA0GCSqG...

MX Record (ако искате да получавате имейли):
Priority: 10
Value: mx.resend.com

CNAME Record:
Host: resend._domainkey
Value: resend._domainkey.yourdomain.com
```

**Забележка**: Проверката на DNS може да отнеме до 48 часа, но обикновено е готова за минути.

## Стъпка 3: Генериране на API Key

1. Отидете в **"API Keys"** в Resend Dashboard
2. Кликнете **"Create API Key"**
3. Дайте име на ключа: `CRM Production` или `CRM Development`
4. Изберете разрешения:
   - **Sending access**: Изпращане на имейли
   - **Domain access**: Четене на домейн настройки
5. Копирайте генерирания ключ (започва с `re_`)

⚠️ **ВАЖНО**: Запазете ключа на сигурно място! Той се показва само веднъж.

## Стъпка 4: Конфигуриране в CRM системата

### Метод А: Глобални настройки (препоръчително за един потребител)

1. Отворете `.env` файла в CRM проекта
2. Добавете следните редове:

```bash
# Resend Email Configuration
RESEND_API_KEY=re_XXXXXXXXXXXXXXXXXXXXXXXXXX
RESEND_FROM_EMAIL=noreply@yourdomain.com
RESEND_FROM_NAME=Вашата Компания
```

3. Рестартирайте сървъра

### Метод Б: Потребителски настройки (за multiple users)

1. Влезте в профила си
2. Отидете на **"Settings"** → **"Resend Email Settings"**
3. Попълнете:
   - **Resend API Key**: Вашият API ключ
   - **From Email**: noreply@yourdomain.com
   - **From Name**: Вашето име или име на компанията

4. Кликнете **"Save"** (Запази)

## Стъпка 5: Тестване

### Тест 1: Изпращане на тестов имейл

1. Създайте тестова фактура с валиден имейл адрес
2. Кликнете **"Send Email to Client"**
3. Изберете шаблон
4. Изпратете

### Проверка на изпращането:

1. Отидете в Resend Dashboard → **"Logs"**
2. Вижте статуса на имейла:
   - ✅ **Delivered**: Успешно доставен
   - ⏳ **Queued**: Изчаква изпращане
   - ❌ **Failed**: Неуспешно

## AI Email Template Studio

CRM системата включва AI генератор на email шаблони:

1. Отидете на **"Template Studio"** → **"Email Templates"**
2. Изберете тип: Invoice, Offer, Custom и др.
3. Въведете AI prompt:
   ```
   Професионален имейл за фактура с модерен дизайн, 
   включващ бутон за плащане и PDF линк
   ```
4. AI генерира красив HTML шаблон автоматично
5. Запазете и използвайте при изпращане

### Template Variables:

В шаблоните можете да използвате:

- `{{client_name}}` - Име на клиента
- `{{invoice_number}}` - Номер на фактурата
- `{{total_amount}}` - Обща сума
- `{{payment_url}}` - Линк за плащане
- `{{pdf_url}}` - Линк за PDF
- `{{sender_name}}` - Вашето име
- И много други...

## SSL Certificate Issues (macOS)

Ако получите SSL грешка при изпращане:

### Решение 1: Install Certificates

```bash
/Applications/Python\ 3.12/Install\ Certificates.command
```

### Решение 2: Install certifi

```bash
cd /path/to/your/project
source venv/bin/activate
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org certifi
```

### Решение 3: Development Fallback

В DEBUG режим, системата автоматично използва Django Console Backend ако има SSL проблем.

## Лимити и цени

### Free Plan:
- **3,000 имейла/месец** безплатно
- Всички функции включени
- Никаква кредитна карта не е нужна

### Pro Plan ($20/месец):
- **50,000 имейла/месец**
- Допълнителни имейли: $1 за 1,000
- Priority support
- Custom IP address

## Често срещани проблеми

### Problem: "Failed to send email: Domain not verified"

**Решение**:
- Проверете дали домейнът е верифициран в Resend
- Изчакайте DNS propagation (до 48 часа)
- Използвайте временно `@resend.dev` адрес за тестване

### Problem: "SSL Certificate Error"

**Решение**:
- Вижте секцията "SSL Certificate Issues" по-горе
- Уверете се, че `certifi` е инсталиран
- Рестартирайте сървъра

### Problem: "Invalid API Key"

**Решение**:
- Проверете дали ключът започва с `re_`
- Уверете се, че няма интервали в началото/края
- Генерирайте нов ключ ако е необходимо

### Problem: "Rate limit exceeded"

**Решение**:
- Достигнали сте месечния лимит
- Upgrade към Pro plan
- Или изчакайте следващия месец

## Email Deliverability (Доставяемост)

За максимална доставяемост:

1. **SPF Record**: Добавете в DNS
   ```
   v=spf1 include:resend.com ~all
   ```

2. **DKIM**: Автоматично настроен от Resend

3. **DMARC**: Добавете за допълнителна сигурност
   ```
   v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
   ```

4. **Warm-up**: Започнете с по-малко имейли и увеличавайте постепенно

## Мониторинг и статистика

В Resend Dashboard можете да видите:

- **Delivery Rate**: % успешно доставени имейли
- **Open Rate**: % отворени имейли (ако е активирано tracking)
- **Click Rate**: % кликнати линкове
- **Bounce Rate**: % върнати имейли
- **Complaint Rate**: % маркирани като spam

## Webhook Integration

За автоматична обработка на събития:

1. В Resend създайте Webhook
2. URL: `https://yourdomain.com/webhooks/resend/`
3. События:
   - `email.delivered` - Доставен
   - `email.opened` - Отворен
   - `email.clicked` - Кликнат
   - `email.bounced` - Върнат
   - `email.complained` - Spam complaint

4. Webhook Secret: Добавете в `.env`

## Поддръжка

- **Resend Docs**: [resend.com/docs](https://resend.com/docs)
- **Resend Support**: support@resend.com
- **CRM Support**: Вашият support имейл

---

**Готово!** Сега можете да изпращате професионални имейли с Resend! 🎉

