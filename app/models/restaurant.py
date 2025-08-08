"""
Модель ресторана
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Restaurant(Base):
    """Модель ресторана"""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Контактная информация
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Адрес и геолокация
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Изображения
    logo_url = Column(String(500), nullable=True)
    cover_url = Column(String(500), nullable=True)
    
    # Рабочие часы
    work_start = Column(Time, nullable=False)
    work_end = Column(Time, nullable=False)
    
    # Доставка
    delivery_fee = Column(Float, default=150.0)
    free_delivery_threshold = Column(Float, default=1000.0)
    max_delivery_distance = Column(Float, default=15.0)  # км
    avg_delivery_time = Column(Integer, default=30)  # минуты
    
    # Статус и рейтинг
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    
    # Статистика
    total_orders = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    menu_items = relationship("MenuItem", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")
    
    def __repr__(self):
        return f"<Restaurant(id={self.id}, name='{self.name}')>"
