from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.service import run_agent
from app.api.routes_agent import router as agent_router
from app.config import get_settings
from app.db.dependencies import get_db

settings = get_settings()


app = FastAPI(
    title="Self-Healing SQL Agent",
    version="0.1.0",
)


class AgentQueryRequest(BaseModel):
    query: str


class AgentQueryResponse(BaseModel):
    query: str
    sql: str | None
    rows: list[dict]
    columns: list[str]

    execution_ms: float

    attempt: int
    max_attempts: int

    llm_calls: int
    repair_attempts: int

    status: str

    error_category: str | None
    error_message: str | None
    diagnosis: str | None

    termination_reason: str | None


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "Self-Healing SQL Agent",
    }
    
app.include_router(agent_router)


@app.post(
    "/api/v1/agent/query",
    response_model=AgentQueryResponse,
)
async def agent_query(
    request: AgentQueryRequest,
    db: AsyncSession = Depends(get_db),
) -> AgentQueryResponse:
    result = await run_agent(
        user_query=request.query,
        db=db,
    )

    return AgentQueryResponse(
        query=request.query,
        sql=result.get("sql"),
        rows=result.get("execution_rows", []),
        columns=result.get("execution_columns", []),
        execution_ms=result.get("execution_ms", 0.0),
        attempt=result.get("attempt", 1),
        max_attempts=result.get("max_attempts", 3),
        llm_calls=result.get("llm_calls", 0),
        repair_attempts=result.get("repair_attempts", 0),
        status=result.get("status", "failed"),
        error_category=result.get("error_category"),
        error_message=result.get("error_message"),
        diagnosis=result.get("diagnosis"),
        termination_reason=result.get(
            "termination_reason"
        ),
    )