from app.agent.nodes.classify import (
    classify_error_message,
)


def test_unknown_column_failure() -> None:
    error = (
        'column "customer_name" '
        'does not exist'
    )

    assert (
        classify_error_message(error)
        == "undefined_column"
    )


def test_unknown_table_failure() -> None:
    error = (
        'relation "customer_accounts" '
        'does not exist'
    )

    assert (
        classify_error_message(error)
        == "undefined_table"
    )