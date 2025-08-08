#!/usr/bin/env python3
"""
Скрипт для запуска FoodDelivery Bot
"""

import asyncio
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🍕 Starting FoodDelivery Bot...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
