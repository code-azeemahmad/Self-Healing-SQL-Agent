
from app.agent.nodes.classify import classify_error_message


def test_classifies_syntax_error() -> None:
    error = 'syntax error at or near "FROM"'

    assert classify_error_message(error) == "syntax_error"


def test_classifies_unknown_column() -> None:
    error = 'column "customer_name" does not exist'

    assert classify_error_message(error) == "undefined_column"


def test_classifies_unknown_table() -> None:
    error = 'relation "customers_archive" does not exist'

    assert classify_error_message(error) == "undefined_table"


def test_classifies_permission_error() -> None:
    error = "permission denied for table customers"

    assert classify_error_message(error) == "permission_error"


def test_classifies_connection_error() -> None:
    error = "connection refused"

    assert classify_error_message(error) == "connection_error"