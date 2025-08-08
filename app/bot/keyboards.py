"""
Клавиатуры для Telegram бота
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def get_main_menu_keyboard():
    """Главное меню бота"""
    keyboard = [
        [InlineKeyboardButton("🍕 Открыть приложение", web_app=WebAppInfo(url="https://your-domain.com/webapp"))],
        [
            InlineKeyboardButton("🏪 Рестораны", callback_data="restaurants_list"),
            InlineKeyboardButton("📋 Мои заказы", callback_data="orders_list")
        ],
        [
            InlineKeyboardButton("🎁 Бонусы", callback_data="loyalty_program"),
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_restaurants_keyboard(restaurants):
    """Клавиатура со списком ресторанов"""
    keyboard = []
    
    for restaurant in restaurants:
        keyboard.append([
            InlineKeyboardButton(
                f"{restaurant.name} ⭐{restaurant.rating}",
                callback_data=f"restaurant_{restaurant.id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)


def get_restaurant_menu_keyboard(restaurant_id, categories):
    """Клавиатура меню ресторана"""
    keyboard = []
    
    for category in categories:
        keyboard.append([
            InlineKeyboardButton(
                category.name,
                callback_data=f"category_{restaurant_id}_{category.id}"
            )
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("🛒 Корзина", callback_data=f"cart_{restaurant_id}")],
        [InlineKeyboardButton("🔙 К ресторанам", callback_data="restaurants_list")]
    ])
    
    return InlineKeyboardMarkup(keyboard)


def get_menu_items_keyboard(restaurant_id, category_id, items):
    """Клавиатура с блюдами категории"""
    keyboard = []
    
    for item in items:
        keyboard.append([
            InlineKeyboardButton(
                f"{item.name} - {item.price}₽",
                callback_data=f"item_{restaurant_id}_{item.id}"
            )
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("🛒 Корзина", callback_data=f"cart_{restaurant_id}")],
        [InlineKeyboardButton("🔙 К меню", callback_data=f"restaurant_{restaurant_id}")]
    ])
    
    return InlineKeyboardMarkup(keyboard)


def get_item_actions_keyboard(restaurant_id, item_id):
    """Клавиатура действий с блюдом"""
    keyboard = [
        [
            InlineKeyboardButton("➖", callback_data=f"decrease_{restaurant_id}_{item_id}"),
            InlineKeyboardButton("1", callback_data=f"quantity_{restaurant_id}_{item_id}"),
            InlineKeyboardButton("➕", callback_data=f"increase_{restaurant_id}_{item_id}")
        ],
        [InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_to_cart_{restaurant_id}_{item_id}")],
        [InlineKeyboardButton("🔙 Назад", callback_data=f"category_{restaurant_id}_back")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cart_keyboard(restaurant_id):
    """Клавиатура корзины"""
    keyboard = [
        [
            InlineKeyboardButton("✏️ Изменить", callback_data=f"edit_cart_{restaurant_id}"),
            InlineKeyboardButton("🗑️ Очистить", callback_data=f"clear_cart_{restaurant_id}")
        ],
        [InlineKeyboardButton("📝 Оформить заказ", callback_data=f"checkout_{restaurant_id}")],
        [InlineKeyboardButton("🔙 К меню", callback_data=f"restaurant_{restaurant_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_checkout_keyboard(restaurant_id):
    """Клавиатура оформления заказа"""
    keyboard = [
        [InlineKeyboardButton("💰 Наличными", callback_data=f"payment_cash_{restaurant_id}")],
        [InlineKeyboardButton("💳 Картой", callback_data=f"payment_card_{restaurant_id}")],
        [InlineKeyboardButton("⭐ Telegram Stars", callback_data=f"payment_stars_{restaurant_id}")],
        [InlineKeyboardButton("🔙 К корзине", callback_data=f"cart_{restaurant_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_order_tracking_keyboard(order_id):
    """Клавиатура отслеживания заказа"""
    keyboard = [
        [InlineKeyboardButton("📍 Показать на карте", callback_data=f"map_{order_id}")],
        [InlineKeyboardButton("📞 Связаться с курьером", callback_data=f"contact_courier_{order_id}")],
        [InlineKeyboardButton("❌ Отменить заказ", callback_data=f"cancel_order_{order_id}")],
        [InlineKeyboardButton("🔙 К заказам", callback_data="orders_list")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_keyboard():
    """Админская клавиатура"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton("🏪 Рестораны", callback_data="admin_restaurants")
        ],
        [
            InlineKeyboardButton("📋 Заказы", callback_data="admin_orders"),
            InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton("🚚 Курьеры", callback_data="admin_couriers"),
            InlineKeyboardButton("💰 Финансы", callback_data="admin_finance")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
