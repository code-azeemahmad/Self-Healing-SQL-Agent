import asyncio
from unittest.mock import patch
from app.db.engine import AsyncSessionLocal
from app.agent.service import run_agent
from app.validation.schemas import SQLGeneration

import pytest
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

@pytest.mark.asyncio
async def test_self_healing_manual():
    print("=" * 60)
    print("MANUAL TEST: Self-Healing SQL Loop with Live Ollama")
    print("=" * 60)
    
    user_query = "Show customer names and their total amount for completed orders"
    print(f"User Query: '{user_query}'\n")

    # Mock initial generation with type error on status = 1:
    async def mock_generate_sql(user_query: str, schema: str):
        print("[Step 1] Initial Generator generated SQL with a type error:")
        sql = "SELECT c.name, o.total_amount FROM customers c JOIN orders o ON c.id = o.customer_id WHERE o.status = 1"
        print(f"   Generated SQL: {sql}\n")
        return SQLGeneration(sql=sql)

    async with AsyncSessionLocal() as db:
        with patch("app.agent.nodes.generate.generate_sql", side_effect=mock_generate_sql):
            print("[Step 2] Executing agent graph...")
            result = await run_agent(user_query=user_query, db=db)

    print("\n" + "=" * 60)
    print("EXECUTION & HEALING REPORT")
    print("=" * 60)
    print(f"- Final Status:       {result.get('status')}")
    print(f"- Termination Reason: {result.get('termination_reason')}")
    print(f"- Total Attempts:     {result.get('attempt')}")
    print(f"- Repair Attempts:    {result.get('repair_attempts')}")
    print(f"- LLM Calls:          {result.get('llm_calls')}")
    print(f"- Execution Time:     {result.get('execution_ms', 0):.2f} ms")
    print(f"- Diagnosis:          {result.get('diagnosis')}")
    print(f"- Repair Reason:      {result.get('repair_reason')}")
    print(f"- Final SQL:          {result.get('sql')}")
    print(f"- Rows Returned:      {len(result.get('execution_rows', []))}")
    print("- Result Rows:")
    for row in result.get("execution_rows", []):
        print(f"   {row}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_self_healing_manual())
