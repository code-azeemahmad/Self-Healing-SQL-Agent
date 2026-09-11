from ollama import AsyncClient

from app.agent.state import AgentState
from app.config import get_settings


async def diagnose_error_node(
    state: AgentState,
) -> dict:
    settings = get_settings()

    client = AsyncClient(
        host=settings.ollama_base_url,
    )

    prompt = f"""
You are diagnosing a PostgreSQL query failure.

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

Explain the likely cause of the SQL failure in one concise paragraph.

Do not propose new SQL.
Do not provide chain-of-thought.
Focus only on the concrete database error.
"""

    response = await client.chat(
        model=settings.ollama_llm_model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "temperature": 0,
        },
    )

    diagnosis = response.message.content

    if not isinstance(diagnosis, str):
        raise TypeError(
            "Ollama returned non-string diagnosis."
        )

    return {
        "diagnosis": diagnosis.strip(),
        "llm_calls": state.get("llm_calls", 0) + 1,
        "status": "repairing",
    }