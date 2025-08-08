"""
API для аутентификации
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.services.auth_service import AuthService

router = APIRouter()


class TelegramAuthData(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    auth_date: int
    hash: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    is_new_user: bool


@router.post("/telegram", response_model=AuthResponse)
async def telegram_auth(
    auth_data: TelegramAuthData,
    db: AsyncSession = Depends(get_db)
):
    """Аутентификация через Telegram"""
    service = AuthService(db)
    
    # Проверяем подлинность данных от Telegram
    if not service.verify_telegram_auth(auth_data.dict()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram authentication data"
        )
    
    # Создаем или получаем пользователя
    user, is_new = await service.get_or_create_user(auth_data)
    
    # Создаем JWT токен
    access_token = service.create_access_token(user.id)
    
    return AuthResponse(
        access_token=access_token,
        user_id=user.id,
        is_new_user=is_new
    )


@router.post("/refresh")
async def refresh_token(
    user_id: int,  # Получаем из текущего токена
    db: AsyncSession = Depends(get_db)
):
    """Обновить токен доступа"""
    service = AuthService(db)
    
    # Проверяем существование пользователя
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Создаем новый токен
    access_token = service.create_access_token(user.id)
    
    return {"access_token": access_token, "token_type": "bearer"}
