"""
Модель отзывов и рейтингов
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Review(Base):
    """Модель отзыва"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    # Связи
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    
    # Рейтинги (1-5)
    rating = Column(Integer, nullable=False)  # Общий рейтинг
    food_rating = Column(Integer, nullable=True)  # Рейтинг еды
    delivery_rating = Column(Integer, nullable=True)  # Рейтинг доставки
    service_rating = Column(Integer, nullable=True)  # Рейтинг сервиса
    
    # Текст отзыва
    comment = Column(Text, nullable=True)
    
    # Статус
    is_approved = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=False)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    order = relationship("Order")
    
    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating}, restaurant_id={self.restaurant_id})>"
