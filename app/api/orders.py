"""
API для работы с заказами
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models import Order, OrderItem, OrderStatus, PaymentMethod
from app.services.order_service import OrderService

router = APIRouter()


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    comment: Optional[str] = None


class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]
    delivery_address: str
    delivery_latitude: Optional[float] = None
    delivery_longitude: Optional[float] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    comment: Optional[str] = None
    payment_method: PaymentMethod = PaymentMethod.CASH


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: OrderStatus
    restaurant_id: int
    subtotal: float
    delivery_fee: float
    discount: float
    total: float
    delivery_address: str
    estimated_delivery_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Создать новый заказ"""
    service = OrderService(db)
    
    try:
        order = await service.create_order(user_id, order_data)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: int,  # Получаем из JWT токена
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Получить заказы пользователя"""
    service = OrderService(db)
    orders = await service.get_user_orders(user_id, skip, limit)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Получить заказ по ID"""
    service = OrderService(db)
    order = await service.get_order(order_id, user_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Обновить статус заказа"""
    service = OrderService(db)
    
    success = await service.update_order_status(order_id, new_status, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found or access denied")
    
    return {"message": "Order status updated successfully"}


@router.delete("/{order_id}")
async def cancel_order(
    order_id: int,
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Отменить заказ"""
    service = OrderService(db)
    
    success = await service.cancel_order(order_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel this order")
    
    return {"message": "Order cancelled successfully"}


@router.get("/{order_id}/track")
async def track_order(
    order_id: int,
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Отследить заказ"""
    service = OrderService(db)
    tracking_info = await service.get_order_tracking(order_id, user_id)
    
    if not tracking_info:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return tracking_info
