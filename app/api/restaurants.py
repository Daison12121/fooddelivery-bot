"""
API для работы с ресторанами
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.models import Restaurant, MenuItem, MenuCategory
from app.services.restaurant_service import RestaurantService

router = APIRouter()


# Pydantic модели для API
class RestaurantResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    address: str
    phone: Optional[str]
    rating: float
    delivery_fee: float
    avg_delivery_time: int
    is_active: bool
    logo_url: Optional[str]
    cover_url: Optional[str]
    
    class Config:
        from_attributes = True


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    weight: Optional[int]
    calories: Optional[int]
    image_url: Optional[str]
    is_available: bool
    is_popular: bool
    is_vegetarian: bool
    
    class Config:
        from_attributes = True


class MenuCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    items: List[MenuItemResponse] = []
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[RestaurantResponse])
async def get_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    max_distance: Optional[float] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Получить список ресторанов"""
    service = RestaurantService(db)
    restaurants = await service.get_restaurants(
        skip=skip,
        limit=limit,
        search=search,
        latitude=latitude,
        longitude=longitude,
        max_distance=max_distance
    )
    return restaurants


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о ресторане"""
    service = RestaurantService(db)
    restaurant = await service.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.get("/{restaurant_id}/menu", response_model=List[MenuCategoryResponse])
async def get_restaurant_menu(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить меню ресторана"""
    service = RestaurantService(db)
    
    # Проверяем существование ресторана
    restaurant = await service.get_restaurant(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Получаем меню
    menu = await service.get_restaurant_menu(restaurant_id)
    return menu


@router.get("/{restaurant_id}/menu/items", response_model=List[MenuItemResponse])
async def get_menu_items(
    restaurant_id: int,
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    vegetarian_only: bool = Query(False),
    available_only: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    """Получить блюда ресторана"""
    service = RestaurantService(db)
    
    items = await service.get_menu_items(
        restaurant_id=restaurant_id,
        category_id=category_id,
        search=search,
        vegetarian_only=vegetarian_only,
        available_only=available_only
    )
    return items


@router.get("/{restaurant_id}/menu/items/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(
    restaurant_id: int,
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить информацию о блюде"""
    service = RestaurantService(db)
    
    item = await service.get_menu_item(restaurant_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    return item


@router.get("/{restaurant_id}/popular", response_model=List[MenuItemResponse])
async def get_popular_items(
    restaurant_id: int,
    limit: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """Получить популярные блюда ресторана"""
    service = RestaurantService(db)
    
    items = await service.get_popular_items(restaurant_id, limit)
    return items
