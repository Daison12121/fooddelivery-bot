"""
Основной Telegram Bot для агрегатора доставки еды
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

from app.core.config import settings
from app.bot.keyboards import get_main_menu_keyboard, get_restaurants_keyboard
from app.bot.handlers import start_handler, restaurants_handler, orders_handler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class FoodDeliveryBot:
    """Основной класс Telegram бота"""
    
    def __init__(self):
        self.application = None
        
    async def setup_bot(self):
        """Настройка и запуск бота"""
        # Создание приложения
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Регистрация обработчиков
        self.application.add_handler(CommandHandler("start", start_handler))
        self.application.add_handler(CallbackQueryHandler(restaurants_handler, pattern="^restaurants"))
        self.application.add_handler(CallbackQueryHandler(orders_handler, pattern="^orders"))
        
        # Запуск бота
        if settings.TELEGRAM_WEBHOOK_URL:
            # Webhook режим для продакшена
            await self.application.bot.set_webhook(
                url=f"{settings.TELEGRAM_WEBHOOK_URL}/webhook",
                allowed_updates=["message", "callback_query"]
            )
        else:
            # Polling режим для разработки
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
        
        logger.info("Bot started successfully!")
        
    async def stop_bot(self):
        """Остановка бота"""
        if self.application:
            await self.application.stop()
            await self.application.shutdown()


# Глобальный экземпляр бота
bot_instance = FoodDeliveryBot()


async def setup_bot():
    """Функция для инициализации бота"""
    await bot_instance.setup_bot()


async def stop_bot():
    """Функция для остановки бота"""
    await bot_instance.stop_bot()


# Обработчики команд
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Создание Web App кнопки
    web_app = WebAppInfo(url="https://your-domain.com/webapp")
    
    keyboard = [
        [InlineKeyboardButton("🍕 Открыть приложение", web_app=web_app)],
        [InlineKeyboardButton("📋 Мои заказы", callback_data="orders_list")],
        [InlineKeyboardButton("🏪 Рестораны", callback_data="restaurants_list")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
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
        reply_markup=reply_markup
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
    
    keyboard = [
        [InlineKeyboardButton("🍕 Pizza Palace", callback_data="restaurant_1")],
        [InlineKeyboardButton("🍔 Burger King", callback_data="restaurant_2")],
        [InlineKeyboardButton("🍜 Суши Мастер", callback_data="restaurant_3")],
        [InlineKeyboardButton("🥗 Healthy Food", callback_data="restaurant_4")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        restaurants_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
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
