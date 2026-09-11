import pytest

from langgraph.graph import END, START, StateGraph

from app.agent.context import AgentContext
from app.agent.nodes.classify import classify_sql_error_node
from app.agent.nodes.diagnose import diagnose_error_node
from app.agent.nodes.execute import execute_sql_node
from app.agent.nodes.repair import repair_sql_node
from app.agent.nodes.validate import validate_sql_node
from app.agent.routing import (
    route_after_classification,
    route_after_execution,
    route_after_validation,
)
from app.agent.state import AgentState
from app.db.engine import AsyncSessionLocal
from app.db.schema import (
    format_schema,
    get_database_schema,
)


def build_recovery_test_graph():
    builder = StateGraph(
        AgentState,
        context_schema=AgentContext,
    )

    builder.add_node(
        "execute_sql",
        execute_sql_node,
    )

    builder.add_node(
        "classify_error",
        classify_sql_error_node,
    )

    builder.add_node(
        "diagnose",
        diagnose_error_node,
    )

    builder.add_node(
        "repair_sql",
        repair_sql_node,
    )

    builder.add_node(
        "validate_sql",
        validate_sql_node,
    )

    builder.add_edge(
        START,
        "execute_sql",
    )

    builder.add_conditional_edges(
        "execute_sql",
        route_after_execution,
        {
            "format_result": END,
            "classify_error": "classify_error",
        },
    )

    builder.add_conditional_edges(
        "classify_error",
        route_after_classification,
        {
            "diagnose": "diagnose",
            "failed": END,
        },
    )

    builder.add_edge(
        "diagnose",
        "repair_sql",
    )

    builder.add_edge(
        "repair_sql",
        "validate_sql",
    )

    builder.add_conditional_edges(
        "validate_sql",
        route_after_validation,
        {
            "execute_sql": "execute_sql",
            "classify_error": "classify_error",
            "failed": END,
        },
    )

    return builder.compile()


@pytest.mark.asyncio
async def test_real_self_healing() -> None:
    async with AsyncSessionLocal() as db:
        schema = await get_database_schema(db)

        state: AgentState = {
            "request_id": "real-self-healing-test",
            "user_query": (
                "Show the customer name"
            ),
            "schema": schema,
            "schema_text": format_schema(schema),

            # Deliberately broken SQL.
            "sql": (
                "SELECT customer_name "
                "FROM customers"
            ),

            "execution_rows": [],
            "execution_columns": [],
            "execution_ms": 0.0,

            "error_category": None,
            "error_message": None,

            "diagnosis": None,
            "repair_reason": None,

            "attempt": 1,
            "max_attempts": 3,

            "llm_calls": 0,
            "repair_attempts": 0,

            "status": "executing",
            "termination_reason": None,
        }

        graph = build_recovery_test_graph()

        result = await graph.ainvoke(
            state,
            context=AgentContext(db=db),
        )

    assert result["status"] == "completed"
    assert result["repair_attempts"] >= 1
    assert result["attempt"] >= 2
    assert result["llm_calls"] >= 2
    assert result["execution_rows"]


@pytest.mark.asyncio
async def test_end_to_end_self_healing_from_raw_query() -> None:
    from app.agent.service import run_agent

    async with AsyncSessionLocal() as db:
        result = await run_agent(
            user_query="SELECT customer_name, country FROM customers;",
            db=db,
        )

    assert result["status"] == "completed"
    assert result["repair_attempts"] >= 1
    assert result["attempt"] >= 2
    assert result["execution_rows"]
    assert "name" in result["execution_columns"] or "customer_name" in result["execution_columns"]
