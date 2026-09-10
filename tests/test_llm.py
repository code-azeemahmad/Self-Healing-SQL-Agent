import pytest

from app.llm.sql_generator import generate_sql


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

    sql = await generate_sql(
        user_query="Show all customers",
        schema=schema,
    )

    assert isinstance(sql, str)
    assert sql.strip()