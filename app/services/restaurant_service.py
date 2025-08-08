"""
Сервис для работы с ресторанами
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from geopy.distance import geodesic

from app.models import Restaurant, MenuItem, MenuCategory


class RestaurantService:
    """Сервис для работы с ресторанами"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_restaurants(
        self,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        max_distance: Optional[float] = None
    ) -> List[Restaurant]:
        """Получить список ресторанов с фильтрацией"""
        
        query = select(Restaurant).where(Restaurant.is_active == True)
        
        # Поиск по названию
        if search:
            query = query.where(
                or_(
                    Restaurant.name.ilike(f"%{search}%"),
                    Restaurant.description.ilike(f"%{search}%")
                )
            )
        
        # Сортировка по рейтингу
        query = query.order_by(Restaurant.rating.desc())
        query = query.offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        restaurants = result.scalars().all()
        
        # Фильтрация по расстоянию (если указаны координаты)
        if latitude and longitude and max_distance:
            filtered_restaurants = []
            user_location = (latitude, longitude)
            
            for restaurant in restaurants:
                restaurant_location = (restaurant.latitude, restaurant.longitude)
                distance = geodesic(user_location, restaurant_location).kilometers
                
                if distance <= max_distance:
                    filtered_restaurants.append(restaurant)
            
            return filtered_restaurants
        
        return list(restaurants)
    
    async def get_restaurant(self, restaurant_id: int) -> Optional[Restaurant]:
        """Получить ресторан по ID"""
        query = select(Restaurant).where(
            and_(
                Restaurant.id == restaurant_id,
                Restaurant.is_active == True
            )
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_restaurant_menu(self, restaurant_id: int) -> List[MenuCategory]:
        """Получить меню ресторана по категориям"""
        query = select(MenuCategory).where(
            and_(
                MenuCategory.restaurant_id == restaurant_id,
                MenuCategory.is_active == True
            )
        ).options(
            selectinload(MenuCategory.menu_items).where(
                MenuItem.is_available == True
            )
        ).order_by(MenuCategory.sort_order)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_menu_items(
        self,
        restaurant_id: int,
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        vegetarian_only: bool = False,
        available_only: bool = True
    ) -> List[MenuItem]:
        """Получить блюда ресторана с фильтрацией"""
        
        query = select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
        
        if available_only:
            query = query.where(MenuItem.is_available == True)
        
        if category_id:
            query = query.where(MenuItem.category_id == category_id)
        
        if search:
            query = query.where(
                or_(
                    MenuItem.name.ilike(f"%{search}%"),
                    MenuItem.description.ilike(f"%{search}%")
                )
            )
        
        if vegetarian_only:
            query = query.where(MenuItem.is_vegetarian == True)
        
        query = query.order_by(MenuItem.sort_order, MenuItem.name)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_menu_item(self, restaurant_id: int, item_id: int) -> Optional[MenuItem]:
        """Получить блюдо по ID"""
        query = select(MenuItem).where(
            and_(
                MenuItem.id == item_id,
                MenuItem.restaurant_id == restaurant_id,
                MenuItem.is_available == True
            )
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_popular_items(self, restaurant_id: int, limit: int = 10) -> List[MenuItem]:
        """Получить популярные блюда ресторана"""
        query = select(MenuItem).where(
            and_(
                MenuItem.restaurant_id == restaurant_id,
                MenuItem.is_available == True,
                MenuItem.is_popular == True
            )
        ).order_by(
            MenuItem.orders_count.desc(),
            MenuItem.rating.desc()
        ).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def calculate_delivery_fee(
        self,
        restaurant_id: int,
        user_latitude: float,
        user_longitude: float,
        order_total: float
    ) -> float:
        """Рассчитать стоимость доставки"""
        
        restaurant = await self.get_restaurant(restaurant_id)
        if not restaurant:
            return 0.0
        
        # Проверяем бесплатную доставку
        if order_total >= restaurant.free_delivery_threshold:
            return 0.0
        
        # Рассчитываем расстояние
        restaurant_location = (restaurant.latitude, restaurant.longitude)
        user_location = (user_latitude, user_longitude)
        distance = geodesic(restaurant_location, user_location).kilometers
        
        # Проверяем максимальное расстояние доставки
        if distance > restaurant.max_delivery_distance:
            return -1  # Доставка невозможна
        
        # Базовая стоимость доставки
        delivery_fee = restaurant.delivery_fee
        
        # Увеличиваем стоимость для дальних расстояний
        if distance > 5:
            delivery_fee += (distance - 5) * 20  # +20₽ за каждый км свыше 5км
        
        return delivery_fee
    
    async def estimate_delivery_time(
        self,
        restaurant_id: int,
        user_latitude: float,
        user_longitude: float
    ) -> int:
        """Оценить время доставки в минутах"""
        
        restaurant = await self.get_restaurant(restaurant_id)
        if not restaurant:
            return 60  # По умолчанию 60 минут
        
        # Базовое время приготовления
        base_time = restaurant.avg_delivery_time
        
        # Рассчитываем расстояние
        restaurant_location = (restaurant.latitude, restaurant.longitude)
        user_location = (user_latitude, user_longitude)
        distance = geodesic(restaurant_location, user_location).kilometers
        
        # Добавляем время на доставку (примерно 2 мин на км)
        delivery_time = int(distance * 2)
        
        return base_time + delivery_time
