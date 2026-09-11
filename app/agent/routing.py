from app.agent.state import AgentState


RECOVERABLE_ERRORS = {
    "syntax_error",
    "undefined_table",
    "undefined_column",
    "invalid_join",
    "type_mismatch",
}


def route_after_validation(
    state: AgentState,
) -> str:
    if state.get("status") == "classifying_error":
        return "classify_error"

    if state.get("status") == "failed":
        return "failed"

    return "execute_sql"


def route_after_execution(
    state: AgentState,
) -> str:
    if state.get("status") == "completed":
        return "format_result"

    return "classify_error"


def route_after_classification(
    state: AgentState,
) -> str:
    category = state.get("error_category")

    if category not in RECOVERABLE_ERRORS:
        return "failed"

    attempt = state.get("attempt", 1)
    max_attempts = state.get("max_attempts", 3)

    if attempt >= max_attempts:
        return "failed"

    return "diagnose"