from langgraph.runtime import Runtime

from app.agent.context import AgentContext
from app.agent.state import AgentState
from app.config import get_settings
from app.db.errors import normalize_database_error
from app.db.executor import execute_sql
from app.validation.query_cost import (
    QueryCostError,
    validate_query_cost,
)


async def execute_sql_node(
    state: AgentState,
    runtime: Runtime[AgentContext],
) -> dict:
    sql = state["sql"] or ""

    try:
        await validate_query_cost(
            session=runtime.context.db,
            sql=sql,
        )

        result = await execute_sql(
            session=runtime.context.db,
            sql=sql,
        )

        return {
            "execution_rows": result.rows,
            "execution_columns": result.columns,
            "execution_ms": result.execution_ms,
            "status": "completed",
            "error_category": None,
            "error_message": None,
            "termination_reason": "successful_execution",
        }

    except QueryCostError as exc:
        return {
            "error_category": "resource_error",
            "error_message": str(exc),
            "status": "classifying_error",
        }

    except Exception as exc:
        error = normalize_database_error(exc)

        return {
            "error_category": error.category,
            "error_message": error.message,
            "status": "classifying_error",
        }