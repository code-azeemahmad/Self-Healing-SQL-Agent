from typing import Any, Literal

from typing_extensions import TypedDict


ErrorCategory = Literal[
    "syntax_error",
    "undefined_table",
    "undefined_column",
    "invalid_join",
    "type_mismatch",
    "permission_error",
    "timeout",
    "connection_error",
    "resource_error",
    "unsafe_sql",
    "unknown_error",
]


AgentStatus = Literal[
    "started",
    "generating",
    "validating",
    "executing",
    "classifying_error",
    "diagnosing",
    "repairing",
    "formatting",
    "completed",
    "failed",
]


class AgentState(TypedDict, total=False):
    request_id: str

    user_query: str

    schema: dict[str, list[str]]
    schema_text: str

    sql: str | None

    execution_rows: list[dict[str, Any]]
    execution_columns: list[str]
    execution_ms: float

    error_category: ErrorCategory | None
    error_message: str | None

    diagnosis: str | None
    repair_reason: str | None

    attempt: int
    max_attempts: int

    llm_calls: int
    repair_attempts: int

    status: AgentStatus

    termination_reason: str | None