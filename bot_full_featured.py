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

# Данные ресторанов и меню
RESTAURANTS = {
    "pizza": {
        "name": "🍕 Pizza Palace",
        "info": "⭐ 4.8 • 🚚 25-35 мин • 💰 от 500₽",
        "menu": [
            {"name": "Маргарита", "desc": "Томаты, моцарелла, базилик", "price": 650},
            {"name": "Пепперони", "desc": "Пепперони, моцарелла, томатный соус", "price": 750},
            {"name": "Четыре сыра", "desc": "4 вида сыра, томатный соус", "price": 850},
            {"name": "Мясная", "desc": "Говядина, свинина, курица", "price": 950}
        ]
    },
    "burger": {
        "name": "🍔 Burger King",
        "info": "⭐ 4.5 • 🚚 20-30 мин • 💰 от 300₽",
        "menu": [
            {"name": "Классический", "desc": "Говяжья котлета, салат, помидор", "price": 450},
            {"name": "Чизбургер", "desc": "Говяжья котлета, сыр, салат", "price": 500},
            {"name": "Биг Бургер", "desc": "Двойная котлета, сыр, бекон", "price": 650},
            {"name": "Куриный", "desc": "Куриная котлета, салат, майонез", "price": 400}
        ]
    },
    "sushi": {
        "name": "🍜 Суши Мастер",
        "info": "⭐ 4.9 • 🚚 30-40 мин • 💰 от 800₽",
        "menu": [
            {"name": "Филадельфия", "desc": "Лосось, сливочный сыр, огурец", "price": 890},
            {"name": "Калифорния", "desc": "Краб, авокадо, огурец, икра", "price": 750},
            {"name": "Дракон", "desc": "Угорь, авокадо, соус унаги", "price": 950},
            {"name": "Сет Мастер", "desc": "Ассорти из 32 роллов", "price": 1200}
        ]
    }
}

# Корзины пользователей
user_carts = {}

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
    
    user = update.effective_user
    user_id = user.id
    
    # Инициализируем корзину пользователя
    if user_id not in user_carts:
        user_carts[user_id] = []
    
    keyboard = [
        [InlineKeyboardButton("🏪 Рестораны", callback_data="restaurants_list")],
        [InlineKeyboardButton("🛒 Корзина", callback_data="cart_view")],
        [InlineKeyboardButton("📋 Мои заказы", callback_data="orders_list")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""🍕 *Добро пожаловать в FoodDelivery Bot!*

Привет, {user.first_name}! 👋

Я помогу тебе заказать вкусную еду из лучших ресторанов города.

🚀 *Что я умею:*
• 🏪 Показывать рестораны и меню
• 🛒 Добавлять блюда в корзину
• 📋 Оформлять заказы
• 📍 Отслеживать доставку

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

Выберите ресторан для просмотра меню:"""

    keyboard = [
        [InlineKeyboardButton("🍕 Pizza Palace", callback_data="menu_pizza")],
        [InlineKeyboardButton("🍔 Burger King", callback_data="menu_burger")],
        [InlineKeyboardButton("🍜 Суши Мастер", callback_data="menu_sushi")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        restaurants_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    restaurant_type = query.data.split("_")[1]  # menu_pizza -> pizza
    restaurant = RESTAURANTS[restaurant_type]
    
    menu_text = f"""🍽️ *Меню {restaurant['name']}*

{restaurant['info']}

📋 *Доступные блюда:*

"""
    
    keyboard = []
    for i, item in enumerate(restaurant['menu']):
        menu_text += f"**{item['name']}** - {item['price']}₽\n_{item['desc']}_\n\n"
        keyboard.append([InlineKeyboardButton(
            f"➕ {item['name']} ({item['price']}₽)", 
            callback_data=f"add_{restaurant_type}_{i}"
        )])
    
    keyboard.append([InlineKeyboardButton("🛒 Корзина", callback_data="cart_view")])
    keyboard.append([InlineKeyboardButton("🔙 К ресторанам", callback_data="restaurants_list")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        menu_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def add_to_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Добавлено в корзину! 🛒")
    
    user_id = query.from_user.id
    data_parts = query.data.split("_")  # add_pizza_0
    restaurant_type = data_parts[1]
    item_index = int(data_parts[2])
    
    restaurant = RESTAURANTS[restaurant_type]
    item = restaurant['menu'][item_index]
    
    # Добавляем в корзину
    if user_id not in user_carts:
        user_carts[user_id] = []
    
    user_carts[user_id].append({
        "restaurant": restaurant['name'],
        "name": item['name'],
        "price": item['price']
    })
    
    logger.info(f"Пользователь {user_id} добавил в корзину: {item['name']}")

async def cart_view_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    cart = user_carts.get(user_id, [])
    
    if not cart:
        cart_text = """🛒 *Ваша корзина пуста*

Добавьте блюда из меню ресторанов!"""
        keyboard = [
            [InlineKeyboardButton("🏪 К ресторанам", callback_data="restaurants_list")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_main")]
        ]
    else:
        cart_text = "🛒 *Ваша корзина:*\n\n"
        total = 0
        
        for item in cart:
            cart_text += f"• {item['name']} - {item['price']}₽\n  _{item['restaurant']}_\n\n"
            total += item['price']
        
        cart_text += f"💰 **Итого: {total}₽**"
        
        keyboard = [
            [InlineKeyboardButton("✅ Оформить заказ", callback_data="checkout")],
            [InlineKeyboardButton("🗑️ Очистить корзину", callback_data="cart_clear")],
            [InlineKeyboardButton("🏪 Добавить еще", callback_data="restaurants_list")],
            [InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_main")]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        cart_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def cart_clear_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Корзина очищена! 🗑️")
    
    user_id = query.from_user.id
    user_carts[user_id] = []
    
    await cart_view_handler(update, context)

async def checkout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    cart = user_carts.get(user_id, [])
    
    if not cart:
        await query.edit_message_text("❌ Корзина пуста!")
        return
    
    total = sum(item['price'] for item in cart)
    order_id = f"#{user_id}{len(cart)}{total}"
    
    # Очищаем корзину после заказа
    user_carts[user_id] = []
    
    order_text = f"""✅ *Заказ оформлен!*

🆔 Номер заказа: {order_id}
💰 Сумма: {total}₽
⏰ Время доставки: 30-45 мин

📍 *Укажите адрес доставки* в следующем сообщении или свяжитесь с поддержкой.

Спасибо за заказ! 🍕"""

    keyboard = [
        [InlineKeyboardButton("📋 Мои заказы", callback_data="orders_list")],
        [InlineKeyboardButton("🏪 Заказать еще", callback_data="restaurants_list")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        order_text, 
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
        [InlineKeyboardButton("🏪 Новый заказ", callback_data="restaurants_list")],
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

🤖 **Как сделать заказ:**

1️⃣ **Выберите ресторан**
   • Нажмите "🏪 Рестораны"
   • Выберите понравившийся ресторан

2️⃣ **Добавьте блюда**
   • Просмотрите меню
   • Нажмите "➕" рядом с блюдом
   • Блюдо добавится в корзину

3️⃣ **Оформите заказ**
   • Перейдите в "🛒 Корзину"
   • Проверьте заказ
   • Нажмите "✅ Оформить заказ"

4️⃣ **Отслеживание**
   • Следите за статусом в "📋 Мои заказы"

🌐 **Дополнительно:**
• API документация: http://localhost:8000/docs
• Веб-версия: http://localhost:8080/webapp.html
• Поддержка: @support_bot"""

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
        [InlineKeyboardButton("🏪 Рестораны", callback_data="restaurants_list")],
        [InlineKeyboardButton("🛒 Корзина", callback_data="cart_view")],
        [InlineKeyboardButton("📋 Мои заказы", callback_data="orders_list")],
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
    print("🤖 Запуск полнофункционального Telegram бота @FoodDeliveryV8_Bot...")
    logger.info("Инициализация бота")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Основные обработчики
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(restaurants_handler, pattern="^restaurants_list$"))
    application.add_handler(CallbackQueryHandler(orders_handler, pattern="^orders_list$"))
    application.add_handler(CallbackQueryHandler(help_handler, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(back_to_main_handler, pattern="^back_to_main$"))
    
    # Обработчики меню
    application.add_handler(CallbackQueryHandler(menu_handler, pattern="^menu_"))
    application.add_handler(CallbackQueryHandler(add_to_cart_handler, pattern="^add_"))
    
    # Обработчики корзины
    application.add_handler(CallbackQueryHandler(cart_view_handler, pattern="^cart_view$"))
    application.add_handler(CallbackQueryHandler(cart_clear_handler, pattern="^cart_clear$"))
    application.add_handler(CallbackQueryHandler(checkout_handler, pattern="^checkout$"))
    
    logger.info("Бот запущен и готов к работе!")
    print("✅ Полнофункциональный бот @FoodDeliveryV8_Bot запущен!")
    print("📱 Найдите бота в Telegram: @FoodDeliveryV8_Bot")
    print("🍕 Функции: меню, корзина, заказы, отслеживание")
    print("🌐 Веб-версия (для разработки): http://localhost:8080/webapp.html")
    print("📖 API документация: http://localhost:8000/docs")
    print("⏹️  Для остановки нажмите Ctrl+C")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
