from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


def normalize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return value


def normalize_row(
    row: dict[str, Any],
) -> tuple[tuple[str, Any], ...]:
    return tuple(
        sorted(
            (
                key,
                normalize_value(value),
            )
            for key, value in row.items()
        )
    )


def normalize_rows(
    rows: list[dict[str, Any]],
) -> list[tuple[tuple[str, Any], ...]]:
    return sorted(
        normalize_row(row)
        for row in rows
    )


async def execute_reference_sql(
    session: AsyncSession,
    reference_sql: str,
) -> list[dict[str, Any]]:
    result = await session.execute(
        text(reference_sql)
    )

    return [
        dict(row)
        for row in result.mappings().all()
    ]


def results_match(
    actual_rows: list[dict[str, Any]],
    expected_rows: list[dict[str, Any]],
) -> bool:
    return (
        normalize_rows(actual_rows)
        == normalize_rows(expected_rows)
    )


async def evaluate_result(
    session: AsyncSession,
    actual_rows: list[dict[str, Any]],
    reference_sql: str,
) -> bool:
    expected_rows = await execute_reference_sql(
        session,
        reference_sql,
    )

    return results_match(
        actual_rows,
        expected_rows,
    )
