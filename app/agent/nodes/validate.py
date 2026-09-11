from app.agent.state import AgentState
from app.validation.schemas import SQLGeneration
from app.validation.sql_guard import (
    MultipleStatementsError,
    SQLGuardError,
    SQLParseError,
    UnknownColumnError,
    UnknownTableError,
    UnsafeStatementError,
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

    except (UnsafeStatementError, MultipleStatementsError) as exc:
        return {
            "error_category": "unsafe_sql",
            "error_message": str(exc),
            "status": "failed",
            "termination_reason": "unsafe_sql_rejected",
        }

    except UnknownColumnError as exc:
        return {
            "error_category": "undefined_column",
            "error_message": str(exc),
            "status": "classifying_error",
        }

    except UnknownTableError as exc:
        return {
            "error_category": "undefined_table",
            "error_message": str(exc),
            "status": "classifying_error",
        }

    except (SQLParseError, SQLGuardError) as exc:
        return {
            "error_category": "syntax_error",
            "error_message": str(exc),
            "status": "classifying_error",
        }