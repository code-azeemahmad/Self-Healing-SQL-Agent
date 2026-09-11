from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.context import AgentContext
from app.agent.graph import build_agent_graph
from app.config import get_settings
from app.db.schema import (
    format_schema,
    get_database_schema,
)


async def run_agent(
    user_query: str,
    db: AsyncSession,
) -> dict:
    settings = get_settings()

    schema = await get_database_schema(db)

    initial_state = {
        "request_id": str(uuid4()),
        "user_query": user_query,
        "schema": schema,
        "schema_text": format_schema(schema),
        "sql": None,
        "execution_rows": [],
        "execution_columns": [],
        "execution_ms": 0.0,
        "error_category": None,
        "error_message": None,
        "diagnosis": None,
        "repair_reason": None,
        "attempt": 1,
        "max_attempts": settings.max_attempts,
        "llm_calls": 0,
        "repair_attempts": 0,
        "status": "started",
        "termination_reason": None,
    }

    graph = build_agent_graph()

    result = await graph.ainvoke(
        initial_state,
        context=AgentContext(db=db),
    )

    return result