
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True,  # Включаем логирование SQL запросов
    future=True,
)

# Создаем фабрику сессий
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для моделей
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 