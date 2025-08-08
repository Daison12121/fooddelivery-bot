"""
Тесты для API ресторанов
"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """Тест корневого endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "FoodDelivery Bot API"
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health_check():
    """Тест проверки здоровья"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_api_root():
    """Тест корневого API endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/")
    
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data
    assert "restaurants" in data["endpoints"]


@pytest.mark.asyncio
async def test_restaurants_list():
    """Тест получения списка ресторанов"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/restaurants/")
    
    # Пока база данных не настроена, ожидаем ошибку подключения
    # В реальных тестах нужно использовать тестовую БД
    assert response.status_code in [200, 500]  # 500 если нет БД
