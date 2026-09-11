from langgraph.graph import END, START, StateGraph

from app.agent.context import AgentContext
from app.agent.nodes.classify import classify_sql_error_node
from app.agent.nodes.diagnose import diagnose_error_node
from app.agent.nodes.execute import execute_sql_node
from app.agent.nodes.format_result import format_result_node
from app.agent.nodes.generate import generate_sql_node
from app.agent.nodes.repair import repair_sql_node
from app.agent.nodes.validate import validate_sql_node
from app.agent.routing import (
    route_after_classification,
    route_after_execution,
    route_after_validation,
)
from app.agent.state import AgentState


def build_agent_graph():
    builder = StateGraph(
        AgentState,
        context_schema=AgentContext,
    )

    builder.add_node(
        "generate_sql",
        generate_sql_node,
    )

    builder.add_node(
        "validate_sql",
        validate_sql_node,
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
        "format_result",
        format_result_node,
    )

    builder.add_edge(
        START,
        "generate_sql",
    )

    builder.add_edge(
        "generate_sql",
        "validate_sql",
    )

    builder.add_conditional_edges(
        "validate_sql",
        route_after_validation,
        {
            "execute_sql": "execute_sql",
            "failed": END,
        },
    )

    builder.add_conditional_edges(
        "execute_sql",
        route_after_execution,
        {
            "format_result": "format_result",
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

    builder.add_edge(
        "format_result",
        END,
    )

    return builder.compile()