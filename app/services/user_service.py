"""
Сервис для работы с пользователями
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Dict, Any

from app.models import User, UserRole


class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_user(self, telegram_id: int, **kwargs) -> User:
        """Создать нового пользователя"""
        user = User(
            telegram_id=telegram_id,
            role=UserRole.CLIENT,
            **kwargs
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def update_user(self, user_id: int, user_data) -> Optional[User]:
        """Обновить данные пользователя"""
        user = await self.get_user(user_id)
        if not user:
            return None
        
        # Обновляем только переданные поля
        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_loyalty_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить информацию о программе лояльности"""
        user = await self.get_user(user_id)
        if not user:
            return None
        
        # Определяем уровень лояльности
        loyalty_level = "Bronze"
        if user.total_orders >= 50:
            loyalty_level = "Gold"
        elif user.total_orders >= 20:
            loyalty_level = "Silver"
        
        # Рассчитываем скидку
        discount_percent = 0
        if loyalty_level == "Gold":
            discount_percent = 10
        elif loyalty_level == "Silver":
            discount_percent = 5
        
        return {
            "user_id": user.id,
            "loyalty_points": user.loyalty_points,
            "total_orders": user.total_orders,
            "total_spent": user.total_spent,
            "loyalty_level": loyalty_level,
            "discount_percent": discount_percent,
            "points_to_next_level": max(0, (20 if loyalty_level == "Bronze" else 50) - user.total_orders)
        }
    
    async def add_loyalty_points(self, user_id: int, points: int) -> bool:
        """Добавить бонусные баллы"""
        user = await self.get_user(user_id)
        if not user:
            return False
        
        user.loyalty_points += points
        await self.db.commit()
        
        return True
    
    async def update_user_stats(self, user_id: int, order_total: float) -> bool:
        """Обновить статистику пользователя после заказа"""
        user = await self.get_user(user_id)
        if not user:
            return False
        
        user.total_orders += 1
        user.total_spent += order_total
        
        # Начисляем бонусные баллы (1 балл за каждые 100 рублей)
        bonus_points = int(order_total // 100)
        user.loyalty_points += bonus_points
        
        await self.db.commit()
        
        return True
