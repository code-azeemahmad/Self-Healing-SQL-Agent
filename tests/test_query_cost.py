import pytest

from app.db.engine import AgentSessionLocal
from app.validation.query_cost import (
    QueryCostError,
    validate_query_cost,
)


@pytest.mark.asyncio
async def test_query_cost_guard_accepts_simple_query() -> None:
    async with AgentSessionLocal() as session:
        await validate_query_cost(
            session,
            "SELECT id, name FROM customers",
        )


@pytest.mark.asyncio
async def test_query_cost_guard_rejects_high_cost_query() -> None:
    async with AgentSessionLocal() as session:
        with pytest.raises(QueryCostError):
            await validate_query_cost(
                session,
                "SELECT * FROM customers",
                max_cost=0.0,
            )
