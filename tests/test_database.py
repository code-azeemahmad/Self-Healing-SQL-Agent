import pytest
from sqlalchemy import text

from app.db.engine import AsyncSessionLocal


@pytest.mark.asyncio
async def test_database_connection() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar_one()

        assert value == 1


from app.db.schema import get_database_schema


@pytest.mark.asyncio
async def test_database_schema() -> None:
    async with AsyncSessionLocal() as session:
        schema = await get_database_schema(session)

        assert "customers" in schema
        assert "orders" in schema
        assert "payments" in schema

        assert "customer_id" in schema["orders"]
        assert "status" in schema["payments"]