from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from typing import Optional, List

# Создать пользователя
async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        role=user_in.role,
        hashed_password=user_in.password,  # Теперь это захешированный пароль
        company_name=user_in.company_name,
        company_description=user_in.company_description,
        bio=user_in.bio,
        social_media_links=user_in.social_media_links,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Получить пользователя по id
async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# Получить пользователя по email
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

# Получить список пользователей
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

# Обновить пользователя
async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user

# Удалить пользователя
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True 