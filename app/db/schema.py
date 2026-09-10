from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_database_schema(
    session: AsyncSession,
) -> dict[str, list[str]]:
    query = text(
        """
        SELECT
            table_name,
            column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name IN (
              'customers',
              'products',
              'orders',
              'order_items',
              'payments',
              'support_tickets'
          )
        ORDER BY table_name, ordinal_position
        """
    )

    result = await session.execute(query)

    schema: dict[str, list[str]] = {}

    for table_name, column_name in result.all():
        schema.setdefault(table_name, []).append(column_name)

    return schema


def format_schema(schema: dict[str, list[str]]) -> str:
    lines: list[str] = []

    for table_name, columns in schema.items():
        lines.append(f"TABLE {table_name}")

        for column in columns:
            lines.append(f"  - {column}")

        lines.append("")

    return "\n".join(lines)