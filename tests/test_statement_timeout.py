import pytest
from sqlalchemy import text

from app.config import get_settings
from app.db.engine import AgentSessionLocal


@pytest.mark.asyncio
async def test_statement_timeout() -> None:
    async with AgentSessionLocal() as session:
        await session.execute(
            text("SET LOCAL statement_timeout = 200")
        )

        with pytest.raises(Exception):
            await session.execute(
                text("SELECT pg_sleep(1)")
            )
