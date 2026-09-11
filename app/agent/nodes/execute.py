from langgraph.runtime import Runtime

from app.agent.context import AgentContext
from app.agent.state import AgentState
from app.db.executor import execute_sql


async def execute_sql_node(
    state: AgentState,
    runtime: Runtime[AgentContext],
) -> dict:
    try:
        result = await execute_sql(
            session=runtime.context.db,
            sql=state["sql"] or "",
        )

        return {
            "execution_rows": result.rows,
            "execution_columns": result.columns,
            "execution_ms": result.execution_ms,
            "status": "formatting",
        }

    except Exception as exc:
        return {
            "error_category": "database_error",
            "error_message": str(exc),
            "status": "failed",
            "termination_reason": "sql_execution_failed",
        }