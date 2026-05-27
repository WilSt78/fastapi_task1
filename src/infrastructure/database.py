from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

from src.core.config import settings

Base = declarative_base()


class Database:
    def __init__(self):
        # Проверяем, что settings имеет атрибут postgres_url
        if not hasattr(settings, 'postgres_url'):
            raise AttributeError("Settings object has no 'postgres_url' attribute")
        
        self._db_url = settings.postgres_url
        self._engine = create_async_engine(
            self._db_url,
            echo=True,
            pool_pre_ping=True,
        )
        self._async_session_maker = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def init_db(self):
        """Создаёт все таблицы (не рекомендуется для production)"""
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    @asynccontextmanager
    async def session(self) -> AsyncSession:
        async with self._async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


# Создаём глобальный экземпляр
database = Database()


async def get_db() -> AsyncSession:
    async with database.session() as session:
        yield session