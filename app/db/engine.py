from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import get_settings


settings = get_settings()


admin_engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    poolclass=NullPool,
)

agent_engine: AsyncEngine = create_async_engine(
    settings.agent_database_url,
    echo=False,
    pool_pre_ping=True,
    poolclass=NullPool,
)


AdminSessionLocal = async_sessionmaker(
    bind=admin_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


AgentSessionLocal = async_sessionmaker(
    bind=agent_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Compatibility alias
AsyncSessionLocal = AgentSessionLocal
engine = agent_engine