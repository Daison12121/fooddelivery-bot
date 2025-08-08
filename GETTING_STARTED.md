# 🍕 FoodDelivery Bot - Инструкция по запуску

## 📋 Что создано

Полнофункциональный агрегатор доставки еды с Telegram Mini App:

### ✅ Готовые компоненты:
- **FastAPI приложение** с REST API
- **Telegram Bot** с основными командами
- **Модели данных** (User, Restaurant, Menu, Order, Courier)
- **Сервисы** для бизнес-логики
- **Docker** конфигурация для развертывания
- **Базовые тесты**

### 🏗️ Архитектура:
`
app/
├── main.py              # Главный файл FastAPI
├── core/                # Конфигурация и БД
├── models/              # SQLAlchemy модели
├── api/                 # REST API endpoints
├── bot/                 # Telegram Bot
└── services/            # Бизнес-логика
`

## 🚀 Быстрый запуск

### 1. Установка зависимостей
`ash
pip install -r requirements.txt
`

### 2. Настройка окружения
`ash
cp .env.example .env
`

Отредактируйте .env файл:
`env
DATABASE_URL=postgresql://user:password@localhost/fooddelivery
REDIS_URL=redis://localhost:6379
TELEGRAM_BOT_TOKEN=your_bot_token_here
SECRET_KEY=your-secret-key-change-in-production
`

### 3. Запуск с Docker (рекомендуется)
`ash
docker-compose up -d
`

### 4. Или запуск локально
`ash
python run.py
`

## 📖 Документация API

После запуска доступна по адресам:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 Основные API endpoints

### Рестораны
- GET /api/v1/restaurants/ - Список ресторанов
- GET /api/v1/restaurants/{id} - Информация о ресторане
- GET /api/v1/restaurants/{id}/menu - Меню ресторана

### Заказы
- POST /api/v1/orders/ - Создать заказ
- GET /api/v1/orders/ - Мои заказы
- GET /api/v1/orders/{id}/track - Отследить заказ

### Пользователи
- GET /api/v1/users/me - Мой профиль
- PATCH /api/v1/users/me - Обновить профиль
- GET /api/v1/users/loyalty - Программа лояльности

### Аутентификация
- POST /api/v1/auth/telegram - Вход через Telegram

## 🤖 Telegram Bot

### Команды:
- /start - Начало работы
- Inline кнопки для навигации
- Web App интеграция

### Функции:
- Каталог ресторанов
- Корзина и заказы
- Отслеживание доставки
- Программа лояльности

## 📊 Что дальше?

### Этап 1: Настройка (1-2 дня)
1. Настроить базу данных PostgreSQL
2. Создать Telegram бота через @BotFather
3. Настроить переменные окружения
4. Запустить приложение

### Этап 2: Наполнение данными (2-3 дня)
1. Добавить рестораны через админку
2. Загрузить меню и фотографии
3. Настроить геолокацию
4. Протестировать заказы

### Этап 3: Telegram Mini App (1-2 недели)
1. Создать React/Vue фронтенд
2. Интегрировать с Telegram Web App
3. Добавить карты и геолокацию
4. Настроить платежи

### Этап 4: Расширенный функционал (2-3 недели)
1. Система курьеров
2. Отслеживание в реальном времени
3. Рейтинги и отзывы
4. Аналитика и отчеты

### Этап 5: Продакшн (1 неделя)
1. Настроить CI/CD
2. Мониторинг и логирование
3. Резервное копирование
4. Масштабирование

## 🛠️ Технологии

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Bot**: python-telegram-bot
- **Cache**: Redis
- **Deploy**: Docker, Nginx
- **Auth**: JWT токены
- **Maps**: Yandex Maps API (опционально)

## 📞 Поддержка

Проект готов к разработке! Все основные компоненты созданы и настроены.

Для запуска нужно только:
1. Установить PostgreSQL и Redis
2. Создать Telegram бота
3. Настроить .env файл
4. Запустить приложение

Удачи в разработке! 🚀
