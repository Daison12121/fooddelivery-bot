"""
Сервис для работы с заказами
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from app.models import Order, OrderItem, MenuItem, Restaurant, User, OrderStatus, PaymentMethod
from app.services.restaurant_service import RestaurantService


class OrderService:
    """Сервис для работы с заказами"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.restaurant_service = RestaurantService(db)
    
    async def create_order(self, user_id: int, order_data) -> Order:
        """Создать новый заказ"""
        
        # Проверяем ресторан
        restaurant = await self.restaurant_service.get_restaurant(order_data.restaurant_id)
        if not restaurant:
            raise ValueError("Restaurant not found")
        
        # Проверяем блюда и рассчитываем сумму
        subtotal = 0.0
        order_items_data = []
        
        for item_data in order_data.items:
            menu_item = await self.restaurant_service.get_menu_item(
                order_data.restaurant_id, 
                item_data.menu_item_id
            )
            if not menu_item:
                raise ValueError(f"Menu item {item_data.menu_item_id} not found")
            
            if not menu_item.is_available:
                raise ValueError(f"Menu item {menu_item.name} is not available")
            
            item_total = menu_item.price * item_data.quantity
            subtotal += item_total
            
            order_items_data.append({
                'menu_item': menu_item,
                'quantity': item_data.quantity,
                'price': menu_item.price,
                'total': item_total,
                'comment': item_data.comment
            })
        
        # Рассчитываем стоимость доставки
        delivery_fee = 0.0
        if order_data.delivery_latitude and order_data.delivery_longitude:
            delivery_fee = await self.restaurant_service.calculate_delivery_fee(
                order_data.restaurant_id,
                order_data.delivery_latitude,
                order_data.delivery_longitude,
                subtotal
            )
            if delivery_fee == -1:
                raise ValueError("Delivery to this address is not available")
        else:
            delivery_fee = restaurant.delivery_fee
        
        # Применяем скидки (пока без скидок)
        discount = 0.0
        total = subtotal + delivery_fee - discount
        
        # Генерируем номер заказа
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        # Оценка времени доставки
        estimated_delivery_time = None
        if order_data.delivery_latitude and order_data.delivery_longitude:
            delivery_minutes = await self.restaurant_service.estimate_delivery_time(
                order_data.restaurant_id,
                order_data.delivery_latitude,
                order_data.delivery_longitude
            )
            estimated_delivery_time = datetime.now() + timedelta(minutes=delivery_minutes)
        
        # Создаем заказ
        order = Order(
            order_number=order_number,
            user_id=user_id,
            restaurant_id=order_data.restaurant_id,
            status=OrderStatus.PENDING,
            payment_method=order_data.payment_method,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            discount=discount,
            total=total,
            delivery_address=order_data.delivery_address,
            delivery_latitude=order_data.delivery_latitude,
            delivery_longitude=order_data.delivery_longitude,
            customer_name=order_data.customer_name,
            customer_phone=order_data.customer_phone,
            comment=order_data.comment,
            estimated_delivery_time=estimated_delivery_time
        )
        
        self.db.add(order)
        await self.db.flush()  # Получаем ID заказа
        
        # Создаем позиции заказа
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item_data['menu_item'].id,
                quantity=item_data['quantity'],
                price=item_data['price'],
                total=item_data['total'],
                comment=item_data['comment']
            )
            self.db.add(order_item)
        
        await self.db.commit()
        await self.db.refresh(order)
        
        return order
    
    async def get_user_orders(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[Order]:
        """Получить заказы пользователя"""
        
        query = select(Order).where(Order.user_id == user_id)\
            .order_by(Order.created_at.desc())\
            .offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_order(self, order_id: int, user_id: int) -> Optional[Order]:
        """Получить заказ по ID"""
        
        query = select(Order).where(
            and_(
                Order.id == order_id,
                Order.user_id == user_id
            )
        ).options(
            selectinload(Order.items).selectinload(OrderItem.menu_item),
            selectinload(Order.restaurant)
        )
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_order_status(
        self, 
        order_id: int, 
        new_status: OrderStatus, 
        user_id: int
    ) -> bool:
        """Обновить статус заказа"""
        
        query = select(Order).where(
            and_(
                Order.id == order_id,
                Order.user_id == user_id
            )
        )
        
        result = await self.db.execute(query)
        order = result.scalar_one_or_none()
        
        if not order:
            return False
        
        # Проверяем возможность изменения статуса
        if not self._can_change_status(order.status, new_status):
            return False
        
        order.status = new_status
        
        # Обновляем временные метки
        if new_status == OrderStatus.CONFIRMED:
            order.confirmed_at = datetime.now()
        elif new_status == OrderStatus.DELIVERED:
            order.delivered_at = datetime.now()
            order.actual_delivery_time = datetime.now()
        
        await self.db.commit()
        return True
    
    async def cancel_order(self, order_id: int, user_id: int) -> bool:
        """Отменить заказ"""
        
        query = select(Order).where(
            and_(
                Order.id == order_id,
                Order.user_id == user_id
            )
        )
        
        result = await self.db.execute(query)
        order = result.scalar_one_or_none()
        
        if not order:
            return False
        
        # Можно отменить только заказы в определенных статусах
        if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            return False
        
        order.status = OrderStatus.CANCELLED
        await self.db.commit()
        return True
    
    async def get_order_tracking(self, order_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить информацию для отслеживания заказа"""
        
        order = await self.get_order(order_id, user_id)
        if not order:
            return None
        
        tracking_info = {
            "order_id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "restaurant": {
                "name": order.restaurant.name,
                "phone": order.restaurant.phone,
                "address": order.restaurant.address
            },
            "delivery_address": order.delivery_address,
            "estimated_delivery_time": order.estimated_delivery_time,
            "actual_delivery_time": order.actual_delivery_time,
            "courier": None,  # Будет добавлено позже
            "timeline": self._get_order_timeline(order)
        }
        
        return tracking_info
    
    def _can_change_status(self, current_status: OrderStatus, new_status: OrderStatus) -> bool:
        """Проверить возможность изменения статуса"""
        
        # Определяем допустимые переходы статусов
        allowed_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.READY],
            OrderStatus.READY: [OrderStatus.DELIVERING],
            OrderStatus.DELIVERING: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],
            OrderStatus.CANCELLED: []
        }
        
        return new_status in allowed_transitions.get(current_status, [])
    
    def _get_order_timeline(self, order: Order) -> List[Dict[str, Any]]:
        """Получить временную линию заказа"""
        
        timeline = [
            {
                "status": "created",
                "title": "Заказ создан",
                "timestamp": order.created_at,
                "completed": True
            }
        ]
        
        if order.confirmed_at:
            timeline.append({
                "status": "confirmed",
                "title": "Заказ подтвержден",
                "timestamp": order.confirmed_at,
                "completed": True
            })
        
        # Добавляем остальные этапы в зависимости от статуса
        status_timeline = {
            OrderStatus.PREPARING: "Готовится",
            OrderStatus.READY: "Готов к выдаче",
            OrderStatus.DELIVERING: "Доставляется",
            OrderStatus.DELIVERED: "Доставлен"
        }
        
        for status, title in status_timeline.items():
            completed = order.status.value >= status.value if hasattr(status, 'value') else False
            timeline.append({
                "status": status.value,
                "title": title,
                "timestamp": order.delivered_at if status == OrderStatus.DELIVERED else None,
                "completed": completed
            })
        
        return timeline
