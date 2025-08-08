"""
Сервис аутентификации
"""

import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models import User
from app.services.user_service import UserService


class AuthService:
    """Сервис аутентификации"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)
    
    def verify_telegram_auth(self, auth_data: Dict[str, Any]) -> bool:
        """Проверить подлинность данных от Telegram"""
        
        # Извлекаем hash из данных
        received_hash = auth_data.pop('hash', '')
        
        # Создаем строку для проверки
        data_check_string = '\n'.join([
            f"{key}={value}" for key, value in sorted(auth_data.items())
        ])
        
        # Создаем секретный ключ
        secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
        
        # Вычисляем hash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Проверяем hash
        if not hmac.compare_digest(calculated_hash, received_hash):
            return False
        
        # Проверяем время (данные должны быть не старше 24 часов)
        auth_date = auth_data.get('auth_date', 0)
        current_time = int(datetime.now().timestamp())
        
        if current_time - auth_date > 86400:  # 24 часа
            return False
        
        return True
    
    async def get_or_create_user(self, auth_data) -> Tuple[User, bool]:
        """Получить или создать пользователя"""
        
        # Ищем существующего пользователя
        user = await self.user_service.get_user_by_telegram_id(auth_data.telegram_id)
        
        if user:
            # Обновляем данные пользователя
            user.username = auth_data.username
            user.first_name = auth_data.first_name
            user.last_name = auth_data.last_name
            user.last_activity = datetime.now()
            
            await self.db.commit()
            await self.db.refresh(user)
            
            return user, False
        
        # Создаем нового пользователя
        user = await self.user_service.create_user(
            telegram_id=auth_data.telegram_id,
            username=auth_data.username,
            first_name=auth_data.first_name,
            last_name=auth_data.last_name,
            last_activity=datetime.now()
        )
        
        return user, True
    
    def create_access_token(self, user_id: int) -> str:
        """Создать JWT токен"""
        
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access"
        }
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[int]:
        """Проверить JWT токен и получить user_id"""
        
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            
            user_id = payload.get("sub")
            if user_id is None:
                return None
            
            return int(user_id)
            
        except JWTError:
            return None
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя (обертка для user_service)"""
        return await self.user_service.get_user(user_id)
