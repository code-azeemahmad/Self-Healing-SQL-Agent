import pytest
from sqlalchemy import text

from app.db.engine import AgentSessionLocal


@pytest.mark.asyncio
async def test_agent_role_cannot_update() -> None:
    async with AgentSessionLocal() as session:
        with pytest.raises(Exception):
            await session.execute(
                text(
                    """
                    UPDATE customers
                    SET name = 'unauthorized'
                    WHERE id = 1
                    """
                )
            )


@pytest.mark.asyncio
async def test_agent_role_cannot_delete() -> None:
    async with AgentSessionLocal() as session:
        with pytest.raises(Exception):
            await session.execute(
                text(
                    "DELETE FROM customers"
                )
            )


@pytest.mark.asyncio
async def test_agent_role_can_select() -> None:
    async with AgentSessionLocal() as session:
        result = await session.execute(
            text(
                "SELECT id, name FROM customers"
            )
        )

        rows = result.mappings().all()

        assert len(rows) > 0
