import pytest
from app.agent.service import run_healing_test
from app.db.engine import AsyncSessionLocal


@pytest.mark.asyncio
async def test_deterministic_self_healing_column_error() -> None:
    """
    Tests that a deliberately broken query (SELECT customer_name FROM customers)
    triggers the full autonomous self-healing loop:
      execute_sql (fails) -> classify_error -> diagnose -> repair_sql -> validate_sql -> execute_sql (succeeds)
    """
    broken_sql = "SELECT customer_name FROM customers;"
    user_query = "Show all customers with their name"

    async with AsyncSessionLocal() as db:
        result = await run_healing_test(
            initial_sql=broken_sql,
            db=db,
            user_query=user_query,
        )

    assert result["status"] == "completed"
    assert result["termination_reason"] == "successful_execution"
    assert result["attempt"] == 2
    assert result["repair_attempts"] == 1
    assert result["diagnosis"]
    assert result["repair_reason"]
    assert result["sql"]
    assert "customer_name" not in result["sql"].lower() or "as customer_name" in result["sql"].lower()
    assert len(result["execution_rows"]) > 0
