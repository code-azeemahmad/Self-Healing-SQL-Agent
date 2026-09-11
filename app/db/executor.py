from __future__ import annotations

import time
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SQLExecutionResult:
    def __init__(
        self,
        rows: list[dict[str, Any]],
        columns: list[str],
        execution_ms: float,
    ) -> None:
        self.rows = rows
        self.columns = columns
        self.execution_ms = execution_ms


async def execute_sql(
    session: AsyncSession,
    sql: str,
) -> SQLExecutionResult:
    started = time.perf_counter()

    result = await session.execute(text(sql))

    rows = [
        dict(row)
        for row in result.mappings().all()
    ]

    columns = list(result.keys())

    execution_ms = (
        time.perf_counter() - started
    ) * 1000

    return SQLExecutionResult(
        rows=rows,
        columns=columns,
        execution_ms=execution_ms,
    )