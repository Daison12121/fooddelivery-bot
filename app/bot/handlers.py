"""
Обработчики команд Telegram бота
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from app.bot.keyboards import get_main_menu_keyboard, get_restaurants_keyboard


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    welcome_text = f"""
🍕 *Добро пожаловать в FoodDelivery Bot!*

Привет, {user.first_name}! 👋

Я помогу тебе заказать вкусную еду из лучших ресторанов города.

🚀 *Что я умею:*
• 📱 Показывать каталог ресторанов
• 🛒 Оформлять заказы
• 📍 Отслеживать доставку
• ⭐ Сохранять твои предпочтения
• 🎁 Начислять бонусы

Нажми на кнопку ниже, чтобы начать! 👇
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu_keyboard()
    )


async def restaurants_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик списка ресторанов"""
    query = update.callback_query
    await query.answer()
    
    # Здесь будет логика получения ресторанов из базы данных
    restaurants_text = """
🏪 *Доступные рестораны:*

🍕 **Pizza Palace**
⭐ 4.8 • 🚚 25-35 мин • 💰 от 500₽

🍔 **Burger King**
⭐ 4.5 • 🚚 20-30 мин • 💰 от 300₽

🍜 **Суши Мастер**
⭐ 4.9 • 🚚 30-40 мин • 💰 от 800₽

🥗 **Healthy Food**
⭐ 4.6 • 🚚 15-25 мин • 💰 от 400₽
    """
    
    # Создаем фиктивные рестораны для демонстрации
    class MockRestaurant:
        def __init__(self, id, name, rating):
            self.id = id
            self.name = name
            self.rating = rating
    
    mock_restaurants = [
        MockRestaurant(1, "🍕 Pizza Palace", 4.8),
        MockRestaurant(2, "🍔 Burger King", 4.5),
        MockRestaurant(3, "🍜 Суши Мастер", 4.9),
        MockRestaurant(4, "🥗 Healthy Food", 4.6),
    ]
    
    await query.edit_message_text(
        restaurants_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_restaurants_keyboard(mock_restaurants)
    )


async def orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик списка заказов"""
    query = update.callback_query
    await query.answer()
    
    orders_text = """
📋 *Мои заказы:*

🟢 **Заказ #1234** - *Доставляется*
🍕 Pizza Margherita x2
📍 ул. Пушкина, 10
⏰ Ожидаемое время: 15 мин

🟡 **Заказ #1233** - *Готовится*
🍔 Big Burger, 🍟 Картофель фри
📍 ул. Ленина, 25
⏰ Ожидаемое время: 25 мин

✅ **Заказ #1232** - *Доставлен*
🍜 Суши сет "Филадельфия"
📍 пр. Мира, 15
⏰ Доставлен вчера в 19:30
    """
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [InlineKeyboardButton("📍 Отследить заказ #1234", callback_data="track_1234")],
        [InlineKeyboardButton("🔄 Повторить заказ #1232", callback_data="repeat_1232")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        orders_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )"""
Обработчики команд Telegram бота
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from app.bot.keyboards import get_main_menu_keyboard, get_restaurants_keyboard


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    welcome_text = f"""
🍕 *Добро пожаловать в FoodDelivery Bot!*

Привет, {user.first_name}! 👋

Я помогу тебе заказать вкусную еду из лучших ресторанов города.

🚀 *Что я умею:*
• 📱 Показывать каталог ресторанов
• 🛒 Оформлять заказы
• 📍 Отслеживать доставку
• ⭐ Сохранять твои предпочтения
• 🎁 Начислять бонусы

Нажми на кнопку ниже, чтобы начать! 👇
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu_keyboard()
    )


async def restaurants_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик списка ресторанов"""
    query = update.callback_query
    await query.answer()
    
    # Здесь будет логика получения ресторанов из базы данных
    restaurants_text = """
🏪 *Доступные рестораны:*

🍕 **Pizza Palace**
⭐ 4.8 • 🚚 25-35 мин • 💰 от 500₽

🍔 **Burger King**
⭐ 4.5 • 🚚 20-30 мин • 💰 от 300₽

🍜 **Суши Мастер**
⭐ 4.9 • 🚚 30-40 мин • 💰 от 800₽

🥗 **Healthy Food**
⭐ 4.6 • 🚚 15-25 мин • 💰 от 400₽
    """
    
    # Создаем фиктивные рестораны для демонстрации
    class MockRestaurant:
        def __init__(self, id, name, rating):
            self.id = id
            self.name = name
            self.rating = rating
    
    mock_restaurants = [
        MockRestaurant(1, "🍕 Pizza Palace", 4.8),
        MockRestaurant(2, "🍔 Burger King", 4.5),
        MockRestaurant(3, "🍜 Суши Мастер", 4.9),
        MockRestaurant(4, "🥗 Healthy Food", 4.6),
    ]
    
    await query.edit_message_text(
        restaurants_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_restaurants_keyboard(mock_restaurants)
    )


async def orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик списка заказов"""
    query = update.callback_query
    await query.answer()
    
    orders_text = """
📋 *Мои заказы:*

🟢 **Заказ #1234** - *Доставляется*
🍕 Pizza Margherita x2
📍 ул. Пушкина, 10
⏰ Ожидаемое время: 15 мин

🟡 **Заказ #1233** - *Готовится*
🍔 Big Burger, 🍟 Картофель фри
📍 ул. Ленина, 25
⏰ Ожидаемое время: 25 мин

✅ **Заказ #1232** - *Доставлен*
🍜 Суши сет "Филадельфия"
📍 пр. Мира, 15
⏰ Доставлен вчера в 19:30
    """
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [InlineKeyboardButton("📍 Отследить заказ #1234", callback_data="track_1234")],
        [InlineKeyboardButton("🔄 Повторить заказ #1232", callback_data="repeat_1232")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        orders_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )