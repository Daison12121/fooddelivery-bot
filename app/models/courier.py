"""
Модель курьера
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class CourierStatus(enum.Enum):
    """Статусы курьера"""
    OFFLINE = "offline"      # Не в сети
    ONLINE = "online"        # В сети, свободен
    BUSY = "busy"           # Занят доставкой
    BREAK = "break"         # На перерыве


class CourierType(enum.Enum):
    """Типы курьеров"""
    STAFF = "staff"         # Штатный сотрудник
    FREELANCER = "freelancer"  # Фрилансер
    PARTNER = "partner"     # Партнер ресторана


class Courier(Base):
    """Модель курьера"""
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связь с пользователем
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Тип и статус
    courier_type = Column(Enum(CourierType), default=CourierType.FREELANCER)
    status = Column(Enum(CourierStatus), default=CourierStatus.OFFLINE)
    
    # Транспорт
    vehicle_type = Column(String(50), nullable=True)  # пешком, велосипед, мотоцикл, автомобиль
    vehicle_number = Column(String(20), nullable=True)
    
    # Документы
    license_number = Column(String(50), nullable=True)
    passport_data = Column(Text, nullable=True)
    
    # Текущее местоположение
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    last_location_update = Column(DateTime(timezone=True), nullable=True)
    
    # Рабочая зона
    work_radius = Column(Float, default=10.0)  # км
    
    # Статистика
    total_deliveries = Column(Integer, default=0)
    successful_deliveries = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    
    # Финансы
    total_earnings = Column(Float, default=0.0)
    commission_rate = Column(Float, default=0.15)  # 15% комиссия
    
    # Статус верификации
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_online = Column(DateTime(timezone=True), nullable=True)
    
    # Связи
    user = relationship("User")
    
    def __repr__(self):
        return f"<Courier(id={self.id}, user_id={self.user_id}, status={self.status})>"


class DeliveryTracking(Base):
    """Отслеживание доставки"""
    __tablename__ = "delivery_tracking"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связи
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=False)
    
    # Координаты
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Дополнительная информация
    speed = Column(Float, nullable=True)  # км/ч
    heading = Column(Float, nullable=True)  # направление в градусах
    accuracy = Column(Float, nullable=True)  # точность в метрах
    
    # Временная метка
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    order = relationship("Order")
    courier = relationship("Courier")
    
    def __repr__(self):
        return f"<DeliveryTracking(order_id={self.order_id}, lat={self.latitude}, lng={self.longitude})>"
