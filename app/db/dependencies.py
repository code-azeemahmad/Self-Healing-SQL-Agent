from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import AgentSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AgentSessionLocal() as session:
        yield session