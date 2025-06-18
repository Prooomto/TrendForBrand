from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db
from app.api.v1.endpoints import auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Подключаем роутеры
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to TrendForBrand Backend!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

@app.get("/health/db")
async def health_check_db(db: AsyncSession = Depends(get_db)):
    try:
        # Выполняем простой запрос для проверки подключения
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
