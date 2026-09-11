from app.agent.routing import (
    route_after_classification,
)


def test_recoverable_error_routes_to_diagnosis() -> None:
    state = {
        "error_category": "undefined_column",
        "attempt": 1,
        "max_attempts": 3,
    }

    assert route_after_classification(state) == "diagnose"


def test_non_recoverable_error_fails() -> None:
    state = {
        "error_category": "permission_error",
        "attempt": 1,
        "max_attempts": 3,
    }

    assert route_after_classification(state) == "failed"


def test_max_attempts_fails() -> None:
    state = {
        "error_category": "undefined_column",
        "attempt": 3,
        "max_attempts": 3,
    }

    assert route_after_classification(state) == "failed"