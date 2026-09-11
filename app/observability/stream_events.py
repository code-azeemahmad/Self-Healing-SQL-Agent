from typing import Any


NODE_EVENT_MAP = {
    "generate_sql": "sql.generated",
    "validate_sql": "validation.updated",
    "execute_sql": "execution.updated",
    "classify_error": "error.classified",
    "diagnose": "diagnosis.completed",
    "repair_sql": "sql.repaired",
    "format_result": "agent.completed",
}


def build_event(
    request_id: str,
    node_name: str,
    update: dict[str, Any],
) -> dict[str, Any]:
    event_name = NODE_EVENT_MAP.get(
        node_name,
        f"node.{node_name}",
    )

    data: dict[str, Any] = {}

    if "sql" in update:
        data["sql"] = update["sql"]

    if "status" in update:
        data["status"] = update["status"]

    if "error_category" in update:
        data["error_category"] = update["error_category"]

    if "error_message" in update:
        data["error_message"] = update["error_message"]

    if "diagnosis" in update:
        data["diagnosis"] = update["diagnosis"]

    if "repair_reason" in update:
        data["repair_reason"] = update["repair_reason"]

    if "attempt" in update:
        data["attempt"] = update["attempt"]

    if "max_attempts" in update:
        data["max_attempts"] = update["max_attempts"]

    if "llm_calls" in update:
        data["llm_calls"] = update["llm_calls"]

    if "repair_attempts" in update:
        data["repair_attempts"] = update["repair_attempts"]

    if "execution_ms" in update:
        data["execution_ms"] = update["execution_ms"]

    if "execution_rows" in update:
        rows = update["execution_rows"]

        data["row_count"] = len(rows)

    if "execution_columns" in update:
        data["columns"] = update["execution_columns"]

    return {
        "request_id": request_id,
        "event": event_name,
        "status": update.get(
            "status",
            "running",
        ),
        "data": data,
    }