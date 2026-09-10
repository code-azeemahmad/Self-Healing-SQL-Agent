import pytest

from app.llm.sql_generator import generate_sql
from app.validation.schemas import SQLGeneration


@pytest.mark.asyncio
async def test_generate_sql() -> None:
    schema = """
    TABLE customers
      - id
      - name
      - email
      - segment
      - country
      - created_at

    TABLE orders
      - id
      - customer_id
      - status
      - total_amount
      - created_at
    """

    result = await generate_sql(
        user_query="Show all customers",
        schema=schema,
    )

    assert isinstance(result, SQLGeneration)
    assert isinstance(result.sql, str)
    assert result.sql.strip()