import pytest
from pydantic import ValidationError

from app.validation.schemas import SQLGeneration


def test_valid_sql_output() -> None:
    result = SQLGeneration(
        sql="SELECT id, name FROM customers"
    )

    assert result.sql == "SELECT id, name FROM customers"


def test_empty_sql_is_rejected() -> None:
    with pytest.raises(ValidationError):
        SQLGeneration(sql="")


def test_extra_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        SQLGeneration(
            sql="SELECT id FROM customers",
            extra_field="invalid_field",  # type: ignore
        )