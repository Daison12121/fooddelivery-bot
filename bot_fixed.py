import asyncio
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "7942867452:AAHUPUnZaKiH-U90hFdnU4Zr3xPlAMBmEh8"

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
    
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🌐 Открыть веб-приложение", url="http://localhost:8000/docs")],
        [InlineKeyboardButton("📋 Мои заказы", callback_data="orders_list")],
        [InlineKeyboardButton("🏪 Рестораны", callback_data="restaurants_list")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""🍕 *Добро пожаловать в FoodDelivery Bot!*

Привет, {user.first_name}! 👋

Я помогу тебе заказать вкусную еду из лучших ресторанов города.

🚀 *Что я умею:*
• 📱 Показывать каталог ресторанов
• 🛒 Оформлять заказы
• 📍 Отслеживать доставку
• ⭐ Сохранять твои предпочтения
• 🎁 Начислять бонусы

Выберите действие из меню ниже! 👇"""

    try:
        await update.message.reply_text(
            welcome_text, 
            parse_mode=ParseMode.MARKDOWN, 
            reply_markup=reply_markup
        )
        logger.info(f"Отправлено приветственное сообщение пользователю {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

async def restaurants_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Обработка запроса ресторанов")
    query = update.callback_query
    await query.answer()
    
    restaurants_text = """🏪 *Доступные рестораны:*

🍕 **Pizza Palace**
⭐ 4.8 • 🚚 25-35 мин • 💰 от 500₽

🍔 **Burger King**
⭐ 4.5 • 🚚 20-30 мин • 💰 от 300₽

🍜 **Суши Мастер**
⭐ 4.9 • 🚚 30-40 мин • 💰 от 800₽

🥗 **Healthy Food**
⭐ 4.6 • 🚚 15-25 мин • 💰 от 400₽"""

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
    logger.info("Обработка запроса заказов")
    query = update.callback_query
    await query.answer()
    
    orders_text = """📋 *Мои заказы:*

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
⏰ Доставлен вчера в 19:30"""

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

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Обработка запроса помощи")
    query = update.callback_query
    await query.answer()
    
    help_text = """ℹ️ *Помощь по использованию бота*

🤖 **Как пользоваться ботом:**

1️⃣ **Выбор ресторана**
   • Нажмите "🏪 Рестораны"
   • Выберите понравившийся ресторан

2️⃣ **Оформление заказа**
   • Просмотрите меню
   • Добавьте блюда в корзину
   • Оформите заказ

3️⃣ **Отслеживание**
   • Следите за статусом в "📋 Мои заказы"
   • Получайте уведомления о готовности

🌐 **Веб-приложение**: http://localhost:8000/docs
📞 **Поддержка:** @support_bot
🕐 **Время работы:** 24/7"""

    keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        help_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def back_to_main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Возврат в главное меню")
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    keyboard = [
        [InlineKeyboardButton("🌐 Открыть веб-приложение", url="http://localhost:8000/docs")],
        [InlineKeyboardButton("📋 Мои заказы", callback_data="orders_list")],
        [InlineKeyboardButton("🏪 Рестораны", callback_data="restaurants_list")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""🍕 *FoodDelivery Bot*

Привет, {user.first_name}! 👋

Выберите действие из меню ниже:"""

    await query.edit_message_text(
        welcome_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

def main():
    print("🤖 Запуск Telegram бота @FoodDeliveryV8_Bot...")
    logger.info("Инициализация бота")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(restaurants_handler, pattern="^restaurants_list$"))
    application.add_handler(CallbackQueryHandler(orders_handler, pattern="^orders_list$"))
    application.add_handler(CallbackQueryHandler(help_handler, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(back_to_main_handler, pattern="^back_to_main$"))
    
    logger.info("Бот запущен и готов к работе!")
    print("✅ Бот @FoodDeliveryV8_Bot успешно запущен!")
    print("📱 Найдите бота в Telegram: @FoodDeliveryV8_Bot")
    print("⏹️  Для остановки нажмите Ctrl+C")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
