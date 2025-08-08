"""
Конфигурация приложения
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    APP_NAME: str = "FoodDelivery Bot"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # База данных
    DATABASE_URL: str = "postgresql://user:password@localhost/fooddelivery"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    
    # Безопасность
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Карты
    YANDEX_MAPS_API_KEY: Optional[str] = None
    
    # Файлы
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Доставка
    DEFAULT_DELIVERY_FEE: float = 150.0
    FREE_DELIVERY_THRESHOLD: float = 1000.0
    MAX_DELIVERY_DISTANCE: float = 15.0  # км
    
    # Рабочие часы
    DEFAULT_WORK_START: str = "09:00"
    DEFAULT_WORK_END: str = "23:00"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создание экземпляра настроек
settings = Settings()
