from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.stream_service import stream_agent, stream_healing_test
from app.db.dependencies import get_db


router = APIRouter(
    prefix="/api/v1/agent",
    tags=["Agent"],
)


class AgentQueryRequest(BaseModel):
    query: str


class HealingTestRequest(BaseModel):
    sql: str = "SELECT customer_name FROM customers;"
    query: str = "Show all customers"


@router.post(
    "/query/stream",
    response_class=EventSourceResponse,
)
async def agent_query_stream(
    request: AgentQueryRequest,
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[ServerSentEvent, None]:

    async for event in stream_agent(
        user_query=request.query,
        db=db,
    ):
        yield ServerSentEvent(
            data=event,
            event=event["event"],
        )


@router.post(
    "/test-healing/stream",
    response_class=EventSourceResponse,
)
async def agent_healing_test_stream(
    request: HealingTestRequest,
    db: AsyncSession = Depends(get_db),
) -> AsyncGenerator[ServerSentEvent, None]:
    async for event in stream_healing_test(
        initial_sql=request.sql,
        db=db,
        user_query=request.query,
    ):
        yield ServerSentEvent(
            data=event,
            event=event["event"],
        )