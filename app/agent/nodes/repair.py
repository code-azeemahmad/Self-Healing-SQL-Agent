from ollama import AsyncClient

from app.agent.state import AgentState
from app.config import get_settings
from app.validation.schemas import SQLRepair


async def repair_sql_node(
    state: AgentState,
) -> dict:
    settings = get_settings()

    client = AsyncClient(
        host=settings.ollama_base_url,
    )

    prompt = f"""
You are repairing a PostgreSQL SELECT query.

User request:
{state["user_query"]}

Database schema:
{state["schema_text"]}

Failed SQL:
{state["sql"]}

Error category:
{state["error_category"]}

Database error:
{state["error_message"]}

Diagnosis:
{state["diagnosis"]}

Repair the failed query so that it answers the original user request.

Rules:

1. Generate exactly one PostgreSQL SELECT statement.
2. Use only tables and columns in the provided schema.
3. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, GRANT, or REVOKE.
4. Do not generate multiple SQL statements.
5. Preserve the original intent of the user's request.
6. Do not invent schema elements.
7. Return structured output matching the provided schema.
"""

    response = await client.chat(
        model=settings.ollama_llm_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format=SQLRepair.model_json_schema(),
        options={
            "temperature": 0,
        },
    )

    content = response.message.content

    if not isinstance(content, str):
        raise TypeError(
            "Ollama returned non-string repair output."
        )

    repair = SQLRepair.model_validate_json(
        content
    )

    return {
        "sql": repair.corrected_sql,
        "diagnosis": repair.diagnosis,
        "repair_reason": repair.repair_reason,
        "llm_calls": state.get("llm_calls", 0) + 1,
        "repair_attempts": state.get("repair_attempts", 0) + 1,
        "attempt": state.get("attempt", 1) + 1,
        "status": "validating",
    }