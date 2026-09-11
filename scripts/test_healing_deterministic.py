import asyncio
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from app.agent.service import run_healing_test
from app.db.engine import AsyncSessionLocal


async def run_deterministic_healing_demo():
    print("=" * 65)
    print("AUTONOMOUS SELF-HEALING SQL AGENT - DETERMINISTIC TEST HARNESS")
    print("=" * 65)

    broken_sql = "SELECT customer_name FROM customers;"
    user_query = "Show all customers"

    print(f"\n[1] Supplying Deliberately Broken SQL:")
    print(f"    SQL:        {broken_sql}")
    print(f"    Intended:   {user_query}\n")

    print("[2] Executing LangGraph Self-Healing Pipeline...")
    print("    • Step 1: execute_sql     -> Fails in PostgreSQL (undefined column 'customer_name')")
    print("    • Step 2: classify_error  -> Classifies as 'undefined_column'")
    print("    • Step 3: diagnose        -> Ollama diagnoses schema discrepancy")
    print("    • Step 4: repair_sql      -> Ollama repairs query (maps 'customer_name' to 'name')")
    print("    • Step 5: validate_sql    -> AST Guardrail re-validates repaired SQL")
    print("    • Step 6: execute_sql     -> Re-executes repaired SQL against PostgreSQL")
    print("    • Step 7: format_result   -> Success!\n")

    async with AsyncSessionLocal() as db:
        result = await run_healing_test(
            initial_sql=broken_sql,
            db=db,
            user_query=user_query,
        )

    print("=" * 65)
    print("FINAL SELF-HEALING EXECUTION REPORT")
    print("=" * 65)
    print(f"• Final Status:          {result.get('status')}")
    print(f"• Termination Reason:    {result.get('termination_reason')}")
    print(f"• Attempts:              {result.get('attempt')} / {result.get('max_attempts')}")
    print(f"• Repair Attempts:       {result.get('repair_attempts')}")
    print(f"• LLM Calls:             {result.get('llm_calls')}")
    print(f"• Execution Time:        {result.get('execution_ms', 0):.2f} ms")
    print(f"\n[DIAGNOSIS]:\n{result.get('diagnosis')}\n")
    print(f"[REPAIR REASON]:\n{result.get('repair_reason')}\n")
    print(f"[FINAL REPAIRED SQL]:\n{result.get('sql')}\n")
    print(f"[ROWS RETURNED ({len(result.get('execution_rows', []))})]:")
    for row in result.get("execution_rows", []):
        print(f"  {row}")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run_deterministic_healing_demo())
