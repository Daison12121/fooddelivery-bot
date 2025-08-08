"""
Основные API роуты
"""

from fastapi import APIRouter
from app.api import auth, restaurants, orders, users, couriers

# Создание основного роутера
api_router = APIRouter()

# Подключение роутеров модулей
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(couriers.router, prefix="/couriers", tags=["couriers"])


@api_router.get("/")
async def api_root():
    """Корневой endpoint API"""
    return {
        "message": "FoodDelivery Bot API v1.0",
        "endpoints": {
            "auth": "/api/v1/auth",
            "restaurants": "/api/v1/restaurants", 
            "orders": "/api/v1/orders",
            "users": "/api/v1/users",
            "couriers": "/api/v1/couriers"
        }
    }
