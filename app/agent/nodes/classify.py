from typing import cast

from app.agent.state import AgentState, ErrorCategory


def classify_error_message(
    error_message: str,
) -> ErrorCategory:
    message = error_message.lower()

    if (
        "syntax error" in message
        or "at or near" in message
    ):
        return "syntax_error"

    if (
        "does not exist" in message
        and "relation" in message
    ):
        return "undefined_table"

    if (
        "does not exist" in message
        and (
            "column" in message
            or "attribute" in message
        )
    ):
        return "undefined_column"

    if (
        "join" in message
        and (
            "operator does not exist" in message
            or "type" in message
        )
    ):
        return "invalid_join"

    if (
        "operator does not exist" in message
        or "cannot cast" in message
        or "invalid input syntax" in message
    ):
        return "type_mismatch"

    if (
        "permission denied" in message
        or "not permitted" in message
    ):
        return "permission_error"

    if (
        "timeout" in message
        or "canceling statement" in message
    ):
        return "timeout"

    if (
        "connection refused" in message
        or "could not connect" in message
        or "connection is closed" in message
    ):
        return "connection_error"

    if (
        "out of memory" in message
        or "remaining connection slots" in message
        or "too many connections" in message
    ):
        return "resource_error"

    return "unknown_error"


def classify_sql_error_node(
    state: AgentState,
) -> dict:
    error_message = state.get(
        "error_message"
    ) or ""

    category = classify_error_message(
        error_message
    )

    return {
        "error_category": cast(
            ErrorCategory,
            category,
        ),
        "status": "classifying_error",
    }