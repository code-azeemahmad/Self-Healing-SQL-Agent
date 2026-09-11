import pytest
from sqlalchemy import text

from app.agent.service import run_agent
from app.db.engine import AsyncSessionLocal


@pytest.mark.asyncio
async def test_agent_query() -> None:
    async with AsyncSessionLocal() as db:
        result = await run_agent(
            user_query="Show all customers",
            db=db,
        )

    assert result["status"] == "completed"
    assert result["sql"]
    assert result["execution_rows"]
    assert result["execution_columns"]