from typing import Literal

from pydantic import BaseModel, ConfigDict


CaseType = Literal[
    "simple",
    "join",
    "aggregation",
    "recoverable",
    "should_fail",
]


class EvaluationCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    question: str
    case_type: CaseType

    expected_success: bool
    recoverable: bool

    reference_sql: str | None = None
    failure_sql: str | None = None

    description: str