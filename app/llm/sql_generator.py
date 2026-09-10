import json

from ollama import AsyncClient
from pydantic import ValidationError

from app.config import get_settings
from app.llm.prompts import SQL_SYSTEM_PROMPT, SQL_USER_PROMPT
from app.validation.schemas import SQLGeneration


async def generate_sql(
    user_query: str,
    schema: str,
) -> SQLGeneration:
    settings = get_settings()

    client = AsyncClient(
        host=settings.ollama_base_url,
    )

    messages = [
        {
            "role": "system",
            "content": SQL_SYSTEM_PROMPT.format(
                schema=schema,
            ),
        },
        {
            "role": "user",
            "content": SQL_USER_PROMPT.format(
                user_query=user_query,
            ),
        },
    ]

    response = await client.chat(
        model=settings.ollama_llm_model,
        messages=messages,
        format=SQLGeneration.model_json_schema(),
        options={
            "temperature": 0,
        },
    )

    content = response.message.content

    if not isinstance(content, str):
        raise TypeError(
            "Ollama returned non-string structured output."
        )

    try:
        return SQLGeneration.model_validate_json(content)
    except ValidationError as exc:
        raise ValueError(
            "LLM produced output that failed SQLGeneration validation."
        ) from exc