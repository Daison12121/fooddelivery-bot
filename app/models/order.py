"""
Модели заказов
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class OrderStatus(enum.Enum):
    """Статусы заказа"""
    PENDING = "pending"          # Ожидает подтверждения
    CONFIRMED = "confirmed"      # Подтвержден рестораном
    PREPARING = "preparing"      # Готовится
    READY = "ready"             # Готов к выдаче
    DELIVERING = "delivering"    # Доставляется
    DELIVERED = "delivered"      # Доставлен
    CANCELLED = "cancelled"      # Отменен


class PaymentMethod(enum.Enum):
    """Способы оплаты"""
    CASH = "cash"               # Наличные
    CARD = "card"               # Банковская карта
    TELEGRAM_STARS = "telegram_stars"  # Telegram Stars
    CRYPTO = "crypto"           # Криптовалюта


class Order(Base):
    """Модель заказа"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Связи
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Статус и оплата
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH)
    is_paid = Column(Boolean, default=False)
    
    # Суммы
    subtotal = Column(Float, nullable=False)  # Сумма блюд
    delivery_fee = Column(Float, default=0.0)  # Стоимость доставки
    discount = Column(Float, default=0.0)     # Скидка
    total = Column(Float, nullable=False)     # Итоговая сумма
    
    # Адрес доставки
    delivery_address = Column(Text, nullable=False)
    delivery_latitude = Column(Float, nullable=True)
    delivery_longitude = Column(Float, nullable=True)
    
    # Контактная информация
    customer_name = Column(String(255), nullable=True)
    customer_phone = Column(String(20), nullable=True)
    
    # Комментарии и заметки
    comment = Column(Text, nullable=True)
    restaurant_notes = Column(Text, nullable=True)
    courier_notes = Column(Text, nullable=True)
    
    # Время
    estimated_delivery_time = Column(DateTime(timezone=True), nullable=True)
    actual_delivery_time = Column(DateTime(timezone=True), nullable=True)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    
    # Связи
    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    restaurant = relationship("Restaurant", back_populates="orders")
    courier = relationship("User", foreign_keys=[courier_id])
    items = relationship("OrderItem", back_populates="order")
    
    def __repr__(self):
        return f"<Order(id={self.id}, number='{self.order_number}', status={self.status})>"


class OrderItem(Base):
    """Позиция в заказе"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связи
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    
    # Количество и цена
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)  # Цена на момент заказа
    total = Column(Float, nullable=False)  # quantity * price
    
    # Комментарии к позиции
    comment = Column(Text, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, quantity={self.quantity}, total={self.total})>"
