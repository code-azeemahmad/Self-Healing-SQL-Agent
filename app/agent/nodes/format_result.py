from app.agent.state import AgentState


async def format_result_node(
    state: AgentState,
) -> dict:
    return {
        "status": "completed",
        "termination_reason": "successful_execution",
    }