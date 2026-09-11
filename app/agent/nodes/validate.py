from app.agent.state import AgentState
from app.validation.schemas import SQLGeneration
from app.validation.sql_guard import (
    SQLGuardError,
    validate_sql,
)


async def validate_sql_node(
    state: AgentState,
) -> dict:
    try:
        generated = SQLGeneration(
            sql=state["sql"] or "",
        )

        validated = validate_sql(
            generated=generated,
            schema=state["schema"],
        )

        return {
            "sql": validated.sql,
            "status": "executing",
        }

    except SQLGuardError as exc:
        return {
            "error_category": "validation_error",
            "error_message": str(exc),
            "status": "failed",
            "termination_reason": "sql_validation_failed",
        }