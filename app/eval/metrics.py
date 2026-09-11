from dataclasses import dataclass
from statistics import mean


@dataclass
class CaseResult:
    case_id: str
    case_type: str

    expected_success: bool
    recoverable: bool

    initial_success: bool
    final_success: bool
    answer_correct: bool

    attempts: int
    repair_attempts: int
    llm_calls: int

    latency_ms: float

    error_category: str | None


@dataclass
class EvaluationMetrics:
    total_cases: int

    initial_success_rate: float
    final_execution_success_rate: float
    answer_accuracy: float
    recovery_rate: float

    average_attempts: float
    p95_latency_ms: float

    total_repairs: int
    total_llm_calls: int


def calculate_p95(
    values: list[float],
) -> float:
    if not values:
        return 0.0

    values = sorted(values)

    index = max(
        0,
        min(
            len(values) - 1,
            round(0.95 * len(values)) - 1,
        ),
    )

    return values[index]


def calculate_metrics(
    results: list[CaseResult],
) -> EvaluationMetrics:
    total = len(results)

    if total == 0:
        return EvaluationMetrics(
            total_cases=0,
            initial_success_rate=0.0,
            final_execution_success_rate=0.0,
            answer_accuracy=0.0,
            recovery_rate=0.0,
            average_attempts=0.0,
            p95_latency_ms=0.0,
            total_repairs=0,
            total_llm_calls=0,
        )

    initial_successes = sum(
        result.initial_success
        for result in results
    )

    final_execution_successes = sum(
        result.final_success
        for result in results
    )

    correct_answers = sum(
        result.answer_correct
        for result in results
    )

    recoverable_failures = [
        result
        for result in results
        if result.recoverable
        and not result.initial_success
    ]

    recovered = sum(
        result.answer_correct
        for result in recoverable_failures
    )

    recovery_rate = (
        recovered / len(recoverable_failures)
        if recoverable_failures
        else 0.0
    )

    latencies = [
        result.latency_ms
        for result in results
    ]

    return EvaluationMetrics(
        total_cases=total,
        initial_success_rate=(
            initial_successes / total
        ),
        final_execution_success_rate=(
            final_execution_successes / total
        ),
        answer_accuracy=(
            correct_answers / total
        ),
        recovery_rate=recovery_rate,
        average_attempts=mean(
            result.attempts
            for result in results
        ),
        p95_latency_ms=calculate_p95(
            latencies
        ),
        total_repairs=sum(
            result.repair_attempts
            for result in results
        ),
        total_llm_calls=sum(
            result.llm_calls
            for result in results
        ),
    )