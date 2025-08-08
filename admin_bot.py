import asyncio
import logging
import os
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "7942867452:AAHUPUnZaKiH-U90hFdnU4Zr3xPlAMBmEh8"

# ID администраторов (замените на ваши Telegram ID)
ADMIN_IDS = [7737197594]  # Добавьте сюда ID администраторов

# Данные системы (в реальном проекте это будет база данных)
RESTAURANTS_DATA = {
    "pizza": {
        "name": "🍕 Pizza Palace",
        "info": "⭐ 4.8 • 🚚 25-35 мин • 💰 от 500₽",
        "active": True,
        "menu": [
            {"id": 1, "name": "Маргарита", "desc": "Томаты, моцарелла, базилик", "price": 650, "active": True},
            {"id": 2, "name": "Пепперони", "desc": "Пепперони, моцарелла, томатный соус", "price": 750, "active": True},
            {"id": 3, "name": "Четыре сыра", "desc": "4 вида сыра, томатный соус", "price": 850, "active": True},
            {"id": 4, "name": "Мясная", "desc": "Говядина, свинина, курица", "price": 950, "active": True}
        ]
    },
    "burger": {
        "name": "🍔 Burger King",
        "info": "⭐ 4.5 • 🚚 20-30 мин • 💰 от 300₽",
        "active": True,
        "menu": [
            {"id": 5, "name": "Классический", "desc": "Говяжья котлета, салат, помидор", "price": 450, "active": True},
            {"id": 6, "name": "Чизбургер", "desc": "Говяжья котлета, сыр, салат", "price": 500, "active": True},
            {"id": 7, "name": "Биг Бургер", "desc": "Двойная котлета, сыр, бекон", "price": 650, "active": True},
            {"id": 8, "name": "Куриный", "desc": "Куриная котлета, салат, майонез", "price": 400, "active": True}
        ]
    }
}

ORDERS_DATA = [
    {"id": 1234, "user_id": 123456, "status": "delivering", "items": ["Pizza Margherita x2"], "total": 1300, "address": "ул. Пушкина, 10"},
    {"id": 1233, "user_id": 789012, "status": "cooking", "items": ["Big Burger", "Картофель фри"], "total": 750, "address": "ул. Ленина, 25"},
    {"id": 1232, "user_id": 345678, "status": "delivered", "items": ["Суши сет Филадельфия"], "total": 890, "address": "пр. Мира, 15"}
]

USERS_DATA = [
    {"id": 123456, "name": "Иван Петров", "orders_count": 5, "total_spent": 3500, "last_order": "2024-01-07"},
    {"id": 789012, "name": "Мария Сидорова", "orders_count": 3, "total_spent": 2100, "last_order": "2024-01-06"},
    {"id": 345678, "name": "Алексей Иванов", "orders_count": 8, "total_spent": 5200, "last_order": "2024-01-05"}
]

def is_admin(user_id):
    return user_id in ADMIN_IDS

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав администратора.")
        return
    
    logger.info(f"Админ {user_id} запустил админ-панель")
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("📋 Заказы", callback_data="admin_orders")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("🏪 Рестораны", callback_data="admin_restaurants")],
        [InlineKeyboardButton("🍽️ Меню", callback_data="admin_menu")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="admin_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    admin_text = f"""🔧 *Админ-панель FoodDelivery*

Добро пожаловать, администратор! 👨‍💼

📊 *Быстрая статистика:*
• Активных заказов: {len([o for o in ORDERS_DATA if o['status'] != 'delivered'])}
• Всего пользователей: {len(USERS_DATA)}
• Активных ресторанов: {len([r for r in RESTAURANTS_DATA.values() if r['active']])}

Выберите раздел для управления:"""

    await update.message.reply_text(
        admin_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def admin_stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ Нет прав доступа")
        return
    
    # Подсчет статистики
    total_orders = len(ORDERS_DATA)
    active_orders = len([o for o in ORDERS_DATA if o['status'] != 'delivered'])
    total_revenue = sum(o['total'] for o in ORDERS_DATA)
    avg_order = total_revenue // total_orders if total_orders > 0 else 0
    
    stats_text = f"""📊 *Статистика системы*

💰 **Финансы:**
• Общая выручка: {total_revenue:,}₽
• Средний чек: {avg_order}₽
• Заказов сегодня: {active_orders}

📋 **Заказы:**
• Всего заказов: {total_orders}
• Активных: {active_orders}
• Доставлено: {total_orders - active_orders}

👥 **Пользователи:**
• Всего пользователей: {len(USERS_DATA)}
• Активных сегодня: {len([u for u in USERS_DATA if u['last_order'] == '2024-01-07'])}

🏪 **Рестораны:**
• Активных ресторанов: {len([r for r in RESTAURANTS_DATA.values() if r['active']])}
• Всего блюд в меню: {sum(len(r['menu']) for r in RESTAURANTS_DATA.values())}

📈 **Топ рестораны:**
• 🍕 Pizza Palace - 45% заказов
• 🍔 Burger King - 35% заказов
• 🍜 Суши Мастер - 20% заказов"""

    keyboard = [
        [InlineKeyboardButton("📊 Обновить", callback_data="admin_stats")],
        [InlineKeyboardButton("📈 Детальная аналитика", callback_data="admin_analytics")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="admin_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        stats_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def admin_orders_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ Нет прав доступа")
        return
    
    orders_text = "📋 *Управление заказами*\n\n"
    
    for order in ORDERS_DATA:
        status_emoji = {"cooking": "🟡", "delivering": "🟢", "delivered": "✅"}
        status_text = {"cooking": "Готовится", "delivering": "Доставляется", "delivered": "Доставлен"}
        
        orders_text += f"{status_emoji.get(order['status'], '⚪')} **Заказ #{order['id']}**\n"
        orders_text += f"Статус: {status_text.get(order['status'], 'Неизвестно')}\n"
        orders_text += f"Сумма: {order['total']}₽\n"
        orders_text += f"Адрес: {order['address']}\n\n"
    
    keyboard = []
    for order in ORDERS_DATA:
        if order['status'] != 'delivered':
            keyboard.append([InlineKeyboardButton(
                f"📝 Заказ #{order['id']}", 
                callback_data=f"order_manage_{order['id']}"
            )])
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="admin_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        orders_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def admin_restaurants_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ Нет прав доступа")
        return
    
    restaurants_text = "🏪 *Управление ресторанами*\n\n"
    
    for rest_id, restaurant in RESTAURANTS_DATA.items():
        status = "✅ Активен" if restaurant['active'] else "❌ Отключен"
        restaurants_text += f"{restaurant['name']}\n"
        restaurants_text += f"Статус: {status}\n"
        restaurants_text += f"Блюд в меню: {len(restaurant['menu'])}\n"
        restaurants_text += f"{restaurant['info']}\n\n"
    
    keyboard = []
    for rest_id, restaurant in RESTAURANTS_DATA.items():
        action = "🔴 Отключить" if restaurant['active'] else "🟢 Включить"
        keyboard.append([InlineKeyboardButton(
            f"{action} {restaurant['name']}", 
            callback_data=f"restaurant_toggle_{rest_id}"
        )])
    
    keyboard.append([InlineKeyboardButton("➕ Добавить ресторан", callback_data="restaurant_add")])
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="admin_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        restaurants_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def restaurant_toggle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    rest_id = query.data.split("_")[2]  # restaurant_toggle_pizza
    restaurant = RESTAURANTS_DATA[rest_id]
    
    # Переключаем статус
    restaurant['active'] = not restaurant['active']
    status = "включен" if restaurant['active'] else "отключен"
    
    await query.answer(f"Ресторан {restaurant['name']} {status}!")
    
    # Возвращаемся к списку ресторанов
    await admin_restaurants_handler(update, context)

async def admin_users_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ Нет прав доступа")
        return
    
    users_text = "👥 *Управление пользователями*\n\n"
    
    for user in USERS_DATA:
        users_text += f"👤 **{user['name']}** (ID: {user['id']})\n"
        users_text += f"Заказов: {user['orders_count']}\n"
        users_text += f"Потрачено: {user['total_spent']}₽\n"
        users_text += f"Последний заказ: {user['last_order']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("📊 Экспорт пользователей", callback_data="users_export")],
        [InlineKeyboardButton("📧 Рассылка", callback_data="users_broadcast")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="admin_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        users_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def order_manage_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    order_id = int(query.data.split("_")[2])  # order_manage_1234
    order = next((o for o in ORDERS_DATA if o['id'] == order_id), None)
    
    if not order:
        await query.edit_message_text("❌ Заказ не найден")
        return
    
    order_text = f"""📋 *Заказ #{order['id']}*

👤 Пользователь: {order['user_id']}
📍 Адрес: {order['address']}
💰 Сумма: {order['total']}₽

🛒 **Состав заказа:**
{chr(10).join(f"• {item}" for item in order['items'])}

📊 **Текущий статус:** {order['status']}"""

    keyboard = []
    if order['status'] == 'cooking':
        keyboard.append([InlineKeyboardButton("🚚 Отправить на доставку", callback_data=f"order_status_{order_id}_delivering")])
    elif order['status'] == 'delivering':
        keyboard.append([InlineKeyboardButton("✅ Отметить доставленным", callback_data=f"order_status_{order_id}_delivered")])
    
    keyboard.append([InlineKeyboardButton("❌ Отменить заказ", callback_data=f"order_cancel_{order_id}")])
    keyboard.append([InlineKeyboardButton("🔙 К заказам", callback_data="admin_orders")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        order_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

async def order_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")  # order_status_1234_delivering
    order_id = int(parts[2])
    new_status = parts[3]
    
    # Находим и обновляем заказ
    for order in ORDERS_DATA:
        if order['id'] == order_id:
            order['status'] = new_status
            break
    
    status_text = {"delivering": "отправлен на доставку", "delivered": "отмечен как доставленный"}
    await query.answer(f"Заказ #{order_id} {status_text.get(new_status, 'обновлен')}!")
    
    # Возвращаемся к управлению заказом
    await order_manage_handler(update, context)

async def admin_main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("📋 Заказы", callback_data="admin_orders")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("🏪 Рестораны", callback_data="admin_restaurants")],
        [InlineKeyboardButton("🍽️ Меню", callback_data="admin_menu")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="admin_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    admin_text = f"""🔧 *Админ-панель FoodDelivery*

📊 *Быстрая статистика:*
• Активных заказов: {len([o for o in ORDERS_DATA if o['status'] != 'delivered'])}
• Всего пользователей: {len(USERS_DATA)}
• Активных ресторанов: {len([r for r in RESTAURANTS_DATA.values() if r['active']])}

Выберите раздел для управления:"""

    await query.edit_message_text(
        admin_text, 
        parse_mode=ParseMode.MARKDOWN, 
        reply_markup=reply_markup
    )

def main():
    print("🔧 Запуск админ-панели FoodDelivery...")
    logger.info("Инициализация админ-бота")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Основные обработчики
    application.add_handler(CommandHandler("admin", start_handler))
    application.add_handler(CallbackQueryHandler(admin_stats_handler, pattern="^admin_stats$"))
    application.add_handler(CallbackQueryHandler(admin_orders_handler, pattern="^admin_orders$"))
    application.add_handler(CallbackQueryHandler(admin_users_handler, pattern="^admin_users$"))
    application.add_handler(CallbackQueryHandler(admin_restaurants_handler, pattern="^admin_restaurants$"))
    application.add_handler(CallbackQueryHandler(admin_main_handler, pattern="^admin_main$"))
    
    # Управление заказами
    application.add_handler(CallbackQueryHandler(order_manage_handler, pattern="^order_manage_"))
    application.add_handler(CallbackQueryHandler(order_status_handler, pattern="^order_status_"))
    
    # Управление ресторанами
    application.add_handler(CallbackQueryHandler(restaurant_toggle_handler, pattern="^restaurant_toggle_"))
    
    logger.info("Админ-панель запущена!")
    print("✅ Админ-панель @FoodDeliveryV8_Bot запущена!")
    print("👨‍💼 Команда для админов: /admin")
    print(f"🔑 ID администраторов: {ADMIN_IDS}")
    print("⏹️  Для остановки нажмите Ctrl+C")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
