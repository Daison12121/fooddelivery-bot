"""
Модели меню и блюд
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class MenuCategory(Base):
    """Категория меню"""
    __tablename__ = "menu_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    restaurant = relationship("Restaurant")
    menu_items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    """Блюдо в меню"""
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Цена и вес
    price = Column(Float, nullable=False)
    weight = Column(Integer, nullable=True)  # граммы
    calories = Column(Integer, nullable=True)
    
    # Изображения
    image_url = Column(String(500), nullable=True)
    
    # Статус
    is_available = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    is_spicy = Column(Boolean, default=False)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    
    # Сортировка и статистика
    sort_order = Column(Integer, default=0)
    orders_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    # Связи
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=True)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    restaurant = relationship("Restaurant", back_populates="menu_items")
    category = relationship("MenuCategory", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")
    
    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', price={self.price})>"
