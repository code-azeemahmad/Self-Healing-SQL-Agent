import asyncio
import json
import time
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.service import run_agent
from app.eval.correctness import evaluate_result
from app.eval.metrics import (
    CaseResult,
    calculate_metrics,
)
from app.eval.recovery import run_recovery_case


DATASET_PATH = (
    Path(__file__).parent / "dataset.json"
)


def load_dataset() -> list[dict]:
    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


async def run_case(
    case: dict,
    db: AsyncSession,
) -> CaseResult:
    started = time.perf_counter()

    result = await run_agent(
        user_query=case["question"],
        db=db,
    )

    latency_ms = (
        time.perf_counter() - started
    ) * 1000

    final_success = (
        result.get("status") == "completed"
    )

    answer_correct = False

    if (
        final_success
        and case.get("reference_sql")
    ):
        answer_correct = (
            await evaluate_result(
                session=db,
                actual_rows=result.get(
                    "execution_rows",
                    [],
                ),
                reference_sql=case[
                    "reference_sql"
                ],
            )
        )

    attempts = result.get(
        "attempt",
        1,
    )

    initial_success = (
        final_success
        and attempts == 1
        and answer_correct
    )

    return CaseResult(
        case_id=case["id"],
        case_type=case["case_type"],
        expected_success=case[
            "expected_success"
        ],
        recoverable=case[
            "recoverable"
        ],
        initial_success=initial_success,
        final_success=final_success,
        answer_correct=answer_correct,
        attempts=attempts,
        repair_attempts=result.get(
            "repair_attempts",
            0,
        ),
        llm_calls=result.get(
            "llm_calls",
            0,
        ),
        latency_ms=latency_ms,
        error_category=result.get(
            "error_category"
        ),
    )


async def run_recovery_case_evaluation(
    case: dict,
    db: AsyncSession,
) -> CaseResult:
    started = time.perf_counter()

    result = await run_recovery_case(
        case,
        db,
    )

    latency_ms = (
        time.perf_counter() - started
    ) * 1000

    final_success = (
        result.get("status") == "completed"
    )

    answer_correct = False

    if (
        final_success
        and case.get("reference_sql")
    ):
        answer_correct = (
            await evaluate_result(
                session=db,
                actual_rows=result.get(
                    "execution_rows",
                    [],
                ),
                reference_sql=case[
                    "reference_sql"
                ],
            )
        )

    return CaseResult(
        case_id=case["id"],
        case_type=case["case_type"],
        expected_success=case[
            "expected_success"
        ],
        recoverable=True,
        initial_success=False,
        final_success=final_success,
        answer_correct=answer_correct,
        attempts=result.get(
            "attempt",
            1,
        ),
        repair_attempts=result.get(
            "repair_attempts",
            0,
        ),
        llm_calls=result.get(
            "llm_calls",
            0,
        ),
        latency_ms=latency_ms,
        error_category=result.get(
            "error_category"
        ),
    )


async def run_evaluation() -> None:
    from app.db.engine import AsyncSessionLocal

    dataset = load_dataset()

    results: list[CaseResult] = []

    async with AsyncSessionLocal() as db:
        for case in dataset:
            print(
                f"Running {case['id']}..."
            )

            if (
                case["case_type"]
                == "recoverable"
                and case.get("failure_sql")
            ):
                result = await run_recovery_case_evaluation(
                    case,
                    db,
                )
            else:
                result = await run_case(
                    case,
                    db,
                )

            results.append(result)

    metrics = calculate_metrics(
        results
    )

    print("\nEvaluation Results")
    print("==================")

    print(
        f"Cases: {metrics.total_cases}"
    )

    print(
        "Initial success rate: "
        f"{metrics.initial_success_rate:.2%}"
    )

    print(
        "Final execution success rate: "
        f"{metrics.final_execution_success_rate:.2%}"
    )

    print(
        "Answer accuracy: "
        f"{metrics.answer_accuracy:.2%}"
    )

    print(
        "Recovery rate: "
        f"{metrics.recovery_rate:.2%}"
    )

    print(
        "Average attempts: "
        f"{metrics.average_attempts:.2f}"
    )

    print(
        "P95 latency: "
        f"{metrics.p95_latency_ms:.2f} ms"
    )

    print(
        f"Repairs: {metrics.total_repairs}"
    )

    print(
        f"LLM calls: {metrics.total_llm_calls}"
    )


if __name__ == "__main__":
    asyncio.run(
        run_evaluation()
    )