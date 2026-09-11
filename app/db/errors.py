from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseError:
    category: str
    message: str
    retryable: bool


def normalize_database_error(
    exc: Exception,
) -> DatabaseError:
    message = str(exc)

    lower_message = message.lower()

    if "does not exist" in lower_message:
        if "column" in lower_message:
            return DatabaseError(
                category="undefined_column",
                message="A referenced column does not exist.",
                retryable=True,
            )

        if "relation" in lower_message:
            return DatabaseError(
                category="undefined_table",
                message="A referenced table does not exist.",
                retryable=True,
            )

    if "syntax error" in lower_message:
        return DatabaseError(
            category="syntax_error",
            message="The generated SQL contains a syntax error.",
            retryable=True,
        )

    if "operator does not exist" in lower_message:
        return DatabaseError(
            category="type_mismatch",
            message="The SQL uses incompatible PostgreSQL types.",
            retryable=True,
        )

    if "permission denied" in lower_message:
        return DatabaseError(
            category="permission_error",
            message="The database role does not have permission for this operation.",
            retryable=False,
        )

    if "timeout" in lower_message or "statement timeout" in lower_message:
        return DatabaseError(
            category="timeout",
            message="The SQL statement exceeded the allowed execution time.",
            retryable=False,
        )

    if (
        "connection refused" in lower_message
        or "connection is closed" in lower_message
        or "could not connect" in lower_message
    ):
        return DatabaseError(
            category="connection_error",
            message="The database connection failed.",
            retryable=False,
        )

    return DatabaseError(
        category="unknown_error",
        message="The database rejected the SQL request.",
        retryable=False,
    )
