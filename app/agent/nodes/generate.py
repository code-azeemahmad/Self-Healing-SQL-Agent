from app.agent.state import AgentState
from app.llm.sql_generator import generate_sql


def is_raw_sql(query: str) -> bool:
    cleaned = query.strip()
    upper = cleaned.upper()
    return upper.startswith("SELECT ") or upper.startswith("WITH ") or upper.startswith("SELECT\n")


async def generate_sql_node(
    state: AgentState,
) -> dict:
    user_query = (state.get("user_query") or "").strip()

    if is_raw_sql(user_query):
        return {
            "sql": user_query,
            "llm_calls": state.get("llm_calls", 0),
            "status": "validating",
        }

    result = await generate_sql(
        user_query=user_query,
        schema=state["schema_text"],
    )

    return {
        "sql": result.sql,
        "llm_calls": state.get("llm_calls", 0) + 1,
        "status": "validating",
    }