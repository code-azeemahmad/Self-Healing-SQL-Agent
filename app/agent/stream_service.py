from collections.abc import AsyncGenerator
from typing import Any
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.context import AgentContext
from app.agent.graph import build_agent_graph
from app.agent.state import AgentState
from app.config import get_settings
from app.db.schema import (
    format_schema,
    get_database_schema,
)
from app.observability.stream_events import build_event


async def stream_agent(
    user_query: str,
    db: AsyncSession,
) -> AsyncGenerator[dict[str, Any], None]:
    settings = get_settings()

    request_id = str(uuid4())

    schema = await get_database_schema(db)

    initial_state: AgentState = {
        "request_id": request_id,
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

    latest_state: dict[str, Any] = dict(
        initial_state
    )

    yield {
        "request_id": request_id,
        "event": "agent.started",
        "status": "started",
        "data": {
            "max_attempts": settings.max_attempts,
        },
    }

    async for chunk in graph.astream(
        initial_state,
        context=AgentContext(db=db),
        stream_mode="updates",
        version="v2",
    ):
        if chunk["type"] != "updates":
            continue

        updates = chunk["data"]

        for node_name, update in updates.items():
            latest_state.update(update)

            event = build_event(
                request_id=request_id,
                node_name=node_name,
                update=update,
            )

            yield event

    yield {
        "request_id": request_id,
        "event": "agent.finished",
        "status": latest_state.get(
            "status",
            "failed",
        ),
        "data": {
            "sql": latest_state.get("sql"),
            "attempt": latest_state.get("attempt", 1),
            "max_attempts": latest_state.get(
                "max_attempts",
                settings.max_attempts,
            ),
            "llm_calls": latest_state.get(
                "llm_calls",
                0,
            ),
            "repair_attempts": latest_state.get(
                "repair_attempts",
                0,
            ),
            "execution_ms": latest_state.get(
                "execution_ms",
                0.0,
            ),
            "row_count": len(
                latest_state.get(
                    "execution_rows",
                    [],
                )
            ),
            "termination_reason": latest_state.get(
                "termination_reason"
            ),
        },
    }