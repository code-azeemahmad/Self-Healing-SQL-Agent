from app.agent.state import AgentState
from app.llm.sql_generator import generate_sql


async def generate_sql_node(
    state: AgentState,
) -> dict:
    result = await generate_sql(
        user_query=state["user_query"],
        schema=state["schema_text"],
    )

    return {
        "sql": result.sql,
        "status": "validating",
    }