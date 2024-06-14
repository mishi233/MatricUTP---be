from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from typing import AsyncGenerator
from db.connection import SessionLocal
from db.base_class import Base

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def create_tables(engine: AsyncEngine) -> None:
    """
        Crea las tablas en la base de datos.

        Nota: Este método se ejecutará al inicializar el servidor, pero solo se crearan las tablas si no existen.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)