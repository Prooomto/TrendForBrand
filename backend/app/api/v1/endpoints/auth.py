from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.auth import register_user, login_user
from app.schemas.users import UserCreate, UserLogin, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await register_user(db, user_in)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при регистрации: {str(e)}"
        )


@router.post("/login", response_model=UserResponse)
async def login(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    try:
        user = await login_user(db, user_credentials)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при входе: {str(e)}"
        ) 