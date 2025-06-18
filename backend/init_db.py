import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import engine, async_session_factory
from app.models.users import Base


async def init_db():
    print("Создание таблиц в базе данных...")
    
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Таблицы успешно созданы!")


async def test_connection():
    print("Тестирование подключения к базе данных...")
    
    try:
        async with async_session_factory() as session:
            # Выполняем простой запрос с использованием text()
            result = await session.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Подключение к базе данных успешно!")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False


async def main():
    print("🚀 Инициализация базы данных TrendForBrand")
    print("=" * 50)
    
    # Тестируем подключение
    if not await test_connection():
        print("\n💡 Убедитесь, что:")
        print("1. PostgreSQL запущен")
        print("2. Файл .env настроен правильно")
        print("3. База данных 'trendforbrand' существует")
        return
    
    # Инициализируем базу данных
    await init_db()
    
    print("\n🎉 База данных готова к использованию!")


if __name__ == "__main__":
    asyncio.run(main()) 