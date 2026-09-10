from langchain_ollama import ChatOllama
from functools import lru_cache
from app.config import get_settings


@lru_cache
def get_llm() -> ChatOllama:
    settings = get_settings()
    return ChatOllama(
        model=settings.ollama_llm_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )