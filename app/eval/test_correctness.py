from app.eval.correctness import results_match


def test_identical_results_match() -> None:
    actual = [
        {"id": 1, "name": "Ali"},
        {"id": 2, "name": "Sara"},
    ]

    expected = [
        {"id": 1, "name": "Ali"},
        {"id": 2, "name": "Sara"},
    ]

    assert results_match(
        actual,
        expected,
    )


def test_different_results_do_not_match() -> None:
    actual = [
        {"id": 1, "name": "Ali"},
    ]

    expected = [
        {"id": 1, "name": "Ali"},
        {"id": 2, "name": "Sara"},
    ]

    assert not results_match(
        actual,
        expected,
    )


def test_row_order_does_not_matter() -> None:
    actual = [
        {"id": 2, "name": "Sara"},
        {"id": 1, "name": "Ali"},
    ]

    expected = [
        {"id": 1, "name": "Ali"},
        {"id": 2, "name": "Sara"},
    ]

    assert results_match(
        actual,
        expected,
    )
