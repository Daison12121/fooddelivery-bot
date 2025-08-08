# 🍕 FoodDelivery Bot - Production Ready

Telegram бот для заказа еды с веб-интерфейсом и админ-панелью.

## 🚀 Возможности

- 🤖 **Telegram бот** с полным функционалом заказов
- 🌐 **Веб-приложение** для пользователей
- 🔧 **Админ-панель** для управления
- 📊 **API** с автоматической документацией
- 🛒 **Корзина** и система заказов
- 📍 **Отслеживание** доставки

## 🛠️ Технологии

- **Backend**: FastAPI + SQLAlchemy
- **Bot**: python-telegram-bot
- **Database**: SQLite (можно заменить на PostgreSQL)
- **Frontend**: HTML/CSS/JavaScript
- **Deploy**: Railway/Render/Fly.io

## 🌐 Развертывание

### Railway (рекомендуется)

1. Создайте аккаунт на [railway.app](https://railway.app)
2. Подключите GitHub репозиторий
3. Установите переменные окружения:
   - `TELEGRAM_BOT_TOKEN`: ваш токен бота
   - `SECRET_KEY`: секретный ключ для приложения
   - `WEBHOOK_URL`: URL вашего приложения + /webhook

### Render

1. Создайте аккаунт на [render.com](https://render.com)
2. Создайте новый Web Service
3. Подключите репозиторий
4. Установите переменные окружения

### Fly.io

1. Установите Fly CLI
2. Выполните `fly launch`
3. Настройте переменные окружения

## 🔧 Переменные окружения

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite+aiosqlite:///./fooddelivery.db
DEBUG=False
WEBHOOK_URL=https://your-app.railway.app/webhook
```

## 📱 Использование

1. Найдите бота в Telegram: @FoodDeliveryV8_Bot
2. Отправьте `/start`
3. Выберите ресторан и добавьте блюда в корзину
4. Оформите заказ

## 🔧 Админ-панель

- **Telegram**: отправьте `/admin` боту
- **Веб**: откройте `/admin.html` на вашем домене

## 📖 API

Документация доступна по адресу `/docs`

## 🤝 Поддержка

Для вопросов и предложений создайте Issue в репозитории.
