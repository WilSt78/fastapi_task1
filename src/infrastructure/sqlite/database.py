from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker  

from .models.baseModel import Base
from .repositories.db_path import db_path as path

db_path = path


class Database:
    def __init__(self):
    
        self._db_url = f"sqlite+aiosqlite:///{db_path}"
        self._engine = create_async_engine(
            self._db_url, 
            connect_args={"check_same_thread": False},
            echo=True
        )

    async def init_db(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @property
    def engine(self):
        return self._engine

    @asynccontextmanager  
    async def session(self): 
        async_session = async_sessionmaker(
            self._engine, 
            expire_on_commit=False
        )
        
        async with async_session() as session: 
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback() 
                raise
            


database = Database()


async def get_db():  
    async with database.session() as session:  
        yield session