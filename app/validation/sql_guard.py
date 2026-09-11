from __future__ import annotations

from dataclasses import dataclass

import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

from app.validation.schemas import SQLGeneration, ValidatedSQL


class SQLGuardError(ValueError):
    """Base exception for SQL policy violations."""


class SQLParseError(SQLGuardError):
    """Raised when SQL cannot be parsed."""


class MultipleStatementsError(SQLGuardError):
    """Raised when more than one SQL statement is supplied."""


class UnsafeStatementError(SQLGuardError):
    """Raised when the SQL statement is not allowed."""


class UnknownTableError(SQLGuardError):
    """Raised when SQL references an unknown table."""


class UnknownColumnError(SQLGuardError):
    """Raised when SQL references an unknown column."""


@dataclass(frozen=True)
class DatabaseSchema:
    tables: dict[str, set[str]]


def _normalize_schema(
    schema: dict[str, list[str]],
) -> DatabaseSchema:
    return DatabaseSchema(
        tables={
            table.lower(): {
                column.lower()
                for column in columns
            }
            for table, columns in schema.items()
        }
    )


def _parse_single_statement(sql: str) -> exp.Expression:
    try:
        statements = sqlglot.parse(
            sql,
            read="postgres",
        )
    except ParseError as exc:
        raise SQLParseError(
            f"Unable to parse SQL: {exc}"
        ) from exc

    if len(statements) != 1:
        raise MultipleStatementsError(
            "Exactly one SQL statement is allowed."
        )

    statement = statements[0]

    if statement is None:
        raise SQLParseError(
            "SQL parser returned an empty statement."
        )

    return statement


def _validate_statement_type(
    statement: exp.Expression,
) -> None:
    if isinstance(statement, exp.Select):
        return

    raise UnsafeStatementError(
        "Only SELECT statements are allowed."
    )


def _validate_tables(
    statement: exp.Expression,
    schema: DatabaseSchema,
) -> None:
    referenced_tables = {
        table.name.lower()
        for table in statement.find_all(exp.Table)
    }

    unknown_tables = referenced_tables - set(schema.tables)

    if unknown_tables:
        names = ", ".join(sorted(unknown_tables))

        raise UnknownTableError(
            f"Unknown table(s): {names}"
        )


def _validate_columns(
    statement: exp.Expression,
    schema: DatabaseSchema,
) -> None:
    known_columns = set().union(
        *schema.tables.values()
    )

    aliases = {
        table.alias_or_name.lower()
        for table in statement.find_all(exp.Table)
    }

    table_by_alias: dict[str, str] = {}

    for table in statement.find_all(exp.Table):
        table_name = table.name.lower()
        alias = table.alias_or_name.lower()

        table_by_alias[alias] = table_name

    for column in statement.find_all(exp.Column):
        column_name = column.name.lower()

        if column_name == "*":
            continue

        table_qualifier = column.table.lower()

        if table_qualifier:
            actual_table = table_by_alias.get(
                table_qualifier,
                table_qualifier,
            )

            if actual_table not in schema.tables:
                raise UnknownTableError(
                    f"Unknown table reference: {table_qualifier}"
                )

            if column_name not in schema.tables[actual_table]:
                raise UnknownColumnError(
                    f"Unknown column '{column_name}' "
                    f"in table '{actual_table}'."
                )

        else:
            if column_name not in known_columns:
                raise UnknownColumnError(
                    f"Unknown column: {column_name}"
                )


def validate_sql(
    generated: SQLGeneration,
    schema: dict[str, list[str]],
) -> ValidatedSQL:
    sql = generated.sql.strip()

    if not sql:
        raise SQLParseError(
            "SQL cannot be empty."
        )

    database_schema = _normalize_schema(schema)

    statement = _parse_single_statement(sql)

    _validate_statement_type(statement)

    _validate_tables(
        statement,
        database_schema,
    )

    _validate_columns(
        statement,
        database_schema,
    )

    normalized_sql = statement.sql(
        dialect="postgres",
    ).strip()

    return ValidatedSQL(
        sql=normalized_sql,
    )