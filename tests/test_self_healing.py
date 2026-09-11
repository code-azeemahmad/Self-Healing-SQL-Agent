import pytest

from app.agent.service import run_agent
from app.db.engine import AsyncSessionLocal


@pytest.mark.asyncio
async def test_agent_completes_successfully() -> None:
    async with AsyncSessionLocal() as db:
        result = await run_agent(
            user_query="Show all customers",
            db=db,
        )

    assert result["status"] == "completed"
    assert result["termination_reason"] == (
        "successful_execution"
    )
    assert result["attempt"] >= 1
    assert result["llm_calls"] >= 1