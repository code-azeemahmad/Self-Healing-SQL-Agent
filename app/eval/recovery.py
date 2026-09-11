from typing import Any

from langgraph.graph import END, START, StateGraph
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.context import AgentContext
from app.agent.nodes.classify import (
    classify_sql_error_node,
)
from app.agent.nodes.diagnose import (
    diagnose_error_node,
)
from app.agent.nodes.execute import (
    execute_sql_node,
)
from app.agent.nodes.repair import (
    repair_sql_node,
)
from app.agent.nodes.validate import (
    validate_sql_node,
)
from app.agent.routing import (
    route_after_classification,
    route_after_execution,
    route_after_validation,
)
from app.agent.state import AgentState
from app.db.schema import (
    format_schema,
    get_database_schema,
)


def build_recovery_graph():
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


async def run_recovery_case(
    case: dict[str, Any],
    db: AsyncSession,
) -> dict[str, Any]:
    schema = await get_database_schema(db)

    state: AgentState = {
        "request_id": f"eval-{case['id']}",
        "user_query": case["question"],
        "schema": schema,
        "schema_text": format_schema(schema),
        "sql": case["failure_sql"],
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

    graph = build_recovery_graph()

    return await graph.ainvoke(
        state,
        context=AgentContext(db=db),
    )
