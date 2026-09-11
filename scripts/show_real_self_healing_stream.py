import asyncio
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from tests.test_real_self_healing import build_recovery_test_graph
from app.agent.context import AgentContext
from app.db.engine import AsyncSessionLocal
from app.db.schema import get_database_schema, format_schema


async def stream_recovery_execution():
    print("=" * 65)
    print("DEMO: LangGraph Real Autonomous Self-Healing Recovery Path")
    print("=" * 65)
    print("Starting LangGraph state with deliberately broken query:")
    print("  SQL: SELECT customer_name FROM customers\n")

    async with AsyncSessionLocal() as db:
        schema = await get_database_schema(db)
        state = {
            "request_id": "inspect-stream-test",
            "user_query": "Show the customer name",
            "schema": schema,
            "schema_text": format_schema(schema),
            "sql": "SELECT customer_name FROM customers",
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

        async for chunk in graph.astream(
            state,
            context=AgentContext(db=db),
            stream_mode="updates",
            version="v2",
        ):
            if chunk["type"] == "updates":
                for node, update in chunk["data"].items():
                    print(f"▶ NODE: [{node}]")
                    if "status" in update:
                        print(f"  • status:           {update['status']}")
                    if "error_category" in update and update["error_category"]:
                        print(f"  • error_category:   {update['error_category']}")
                    if "diagnosis" in update and update["diagnosis"]:
                        print(f"  • diagnosis:        {update['diagnosis']}")
                    if "repair_reason" in update and update["repair_reason"]:
                        print(f"  • repair_reason:    {update['repair_reason']}")
                    if "sql" in update and update["sql"]:
                        print(f"  • sql:              {update['sql']}")
                    if "attempt" in update:
                        print(f"  • attempt:          {update['attempt']}")
                    if "repair_attempts" in update:
                        print(f"  • repair_attempts:   {update['repair_attempts']}")
                    if "execution_rows" in update:
                        print(f"  • execution_rows:   {len(update['execution_rows'])} rows returned")
                    print()

        print("=" * 65)
        print("Self-healing completed successfully.")
        print("=" * 65)


if __name__ == "__main__":
    asyncio.run(stream_recovery_execution())
