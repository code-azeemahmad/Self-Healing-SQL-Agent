from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class QueryCostError(ValueError):
    pass


async def validate_query_cost(
    session: AsyncSession,
    sql: str,
    max_cost: float = 10_000.0,
) -> None:
    try:
        result = await session.execute(
            text(
                f"EXPLAIN (FORMAT JSON) {sql}"
            )
        )

        plan = result.scalar_one()

        if not isinstance(plan, list):
            raise QueryCostError(
                "Unable to inspect PostgreSQL query plan."
            )

        root = plan[0].get("Plan", {})

        total_cost = root.get(
            "Total Cost",
            0,
        )

        if total_cost > max_cost:
            raise QueryCostError(
                "Query exceeds the configured execution-cost threshold."
            )
    except QueryCostError:
        raise
    except Exception:
        await session.rollback()
        raise
