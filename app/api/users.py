"""
API для работы с пользователями
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.models import User, UserRole
from app.services.user_service import UserService

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    role: UserRole
    loyalty_points: int
    total_orders: int
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о текущем пользователе"""
    service = UserService(db)
    user = await service.get_user(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Обновить информацию о текущем пользователе"""
    service = UserService(db)
    user = await service.update_user(user_id, user_data)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/loyalty")
async def get_loyalty_info(
    user_id: int,  # Получаем из JWT токена
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о программе лояльности"""
    service = UserService(db)
    loyalty_info = await service.get_loyalty_info(user_id)
    
    if not loyalty_info:
        raise HTTPException(status_code=404, detail="User not found")
    
    return loyalty_info
