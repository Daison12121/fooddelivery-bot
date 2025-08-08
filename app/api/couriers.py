"""
API для курьеров (заглушка)
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_couriers():
    """Получить список курьеров"""
    return {"message": "Couriers API - coming soon"}


@router.get("/{courier_id}")
async def get_courier(courier_id: int):
    """Получить информацию о курьере"""
    return {"message": f"Courier {courier_id} info - coming soon"}
