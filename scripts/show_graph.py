from app.agent.graph import build_agent_graph


graph = build_agent_graph()

print(
    graph.get_graph().draw_mermaid()
)