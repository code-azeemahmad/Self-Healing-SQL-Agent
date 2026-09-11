import pytest

from app.validation.schemas import SQLGeneration
from app.validation.sql_guard import (
    MultipleStatementsError,
    SQLParseError,
    UnknownColumnError,
    UnknownTableError,
    UnsafeStatementError,
    validate_sql,
)


SCHEMA = {
    "customers": {
        "id",
        "name",
        "email",
        "segment",
        "country",
        "created_at",
    },
    "orders": {
        "id",
        "customer_id",
        "status",
        "total_amount",
        "created_at",
    },
    "payments": {
        "id",
        "order_id",
        "status",
        "amount",
        "payment_method",
        "created_at",
    },
}

def test_valid_select_is_accepted() -> None:
    generated = SQLGeneration(
        sql="SELECT id, name FROM customers"
    )

    result = validate_sql(
        generated,
        SCHEMA,
    )

    assert result.sql


def test_delete_is_rejected() -> None:
    generated = SQLGeneration(
        sql="DELETE FROM customers"
    )

    with pytest.raises(UnsafeStatementError):
        validate_sql(
            generated,
            SCHEMA,
        )


def test_update_is_rejected() -> None:
    generated = SQLGeneration(
        sql="UPDATE customers SET name = 'x'"
    )

    with pytest.raises(UnsafeStatementError):
        validate_sql(
            generated,
            SCHEMA,
        )


def test_drop_is_rejected() -> None:
    generated = SQLGeneration(
        sql="DROP TABLE customers"
    )

    with pytest.raises(UnsafeStatementError):
        validate_sql(
            generated,
            SCHEMA,
        )

    
def test_unknown_table_is_rejected() -> None:
    generated = SQLGeneration(
        sql="SELECT * FROM customer_accounts"
    )

    with pytest.raises(UnknownTableError):
        validate_sql(
            generated,
            SCHEMA,
        )

def test_unknown_column_is_rejected() -> None:
    generated = SQLGeneration(
        sql="SELECT customer_name FROM customers"
    )

    with pytest.raises(UnknownColumnError):
        validate_sql(
            generated,
            SCHEMA,
        )


def test_multiple_statements_are_rejected() -> None:
    generated = SQLGeneration(
        sql="""
        SELECT * FROM customers;
        SELECT * FROM payments;
        """
    )

    with pytest.raises(MultipleStatementsError):
        validate_sql(
            generated,
            SCHEMA,
        )


def test_invalid_sql_is_rejected() -> None:
    generated = SQLGeneration(
        sql="SELECT FROM"
    )

    with pytest.raises(SQLParseError):
        validate_sql(
            generated,
            SCHEMA,
        )