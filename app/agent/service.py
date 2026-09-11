from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.context import AgentContext
from app.agent.graph import build_agent_graph
from app.db.schema import format_schema, get_database_schema


async def run_agent(
    user_query: str,
    db: AsyncSession,
) -> dict:
    schema = await get_database_schema(db)

    initial_state = {
        "request_id": str(uuid4()),
        "user_query": user_query,
        "schema": schema,
        "schema_text": format_schema(schema),
        "status": "started",
    }

    graph = build_agent_graph()

    result = await graph.ainvoke(
        initial_state,
        context=AgentContext(db=db),
    )

    return result