from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.dependencies import get_db
from app.db.schema import format_schema, get_database_schema
from app.llm.sql_generator import generate_sql


settings = get_settings()

app = FastAPI(
    title="Self-Healing SQL Agent",
    version="0.1.0",
)


class SQLGenerationRequest(BaseModel):
    query: str


class SQLGenerationResponse(BaseModel):
    query: str
    sql: str


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "Self-Healing SQL Agent",
    }


@app.post(
    "/api/v1/sql/generate",
    response_model=SQLGenerationResponse,
)
async def generate_sql_endpoint(
    request: SQLGenerationRequest,
    db: AsyncSession = Depends(get_db),
) -> SQLGenerationResponse:
    schema = await get_database_schema(db)
    schema_text = format_schema(schema)

    generated = await generate_sql(
        user_query=request.query,
        schema=schema_text,
    )

    return SQLGenerationResponse(
        query=request.query,
        sql=generated.sql,
    )