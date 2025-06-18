from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.users import create_user, get_user_by_email
from app.schemas.users import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status


async def register_user(db: AsyncSession, user_in: UserCreate):
    
    # Проверяем, не существует ли уже пользователь с таким email
    existing_user = await get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    # Хешируем пароль
    hashed_password = get_password_hash(user_in.password)
    
    # Создаем объект пользователя с захешированным паролем
    user_data = user_in.model_copy()
    user_data.password = hashed_password
    
    # Создаем пользователя в базе данных
    user = await create_user(db, user_data)
    
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    
    # Получаем пользователя по email
    user = await get_user_by_email(db, email)
    if not user:
        return None
    
    # Проверяем пароль
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


async def login_user(db: AsyncSession, user_credentials: UserLogin):
    
    # Аутентифицируем пользователя
    user = await authenticate_user(db, user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь неактивен"
        )
    
    return user 