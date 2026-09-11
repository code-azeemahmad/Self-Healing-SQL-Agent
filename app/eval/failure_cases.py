FAILURE_CASES = {
    "column_error": {
        "sql": (
            "SELECT customer_name "
            "FROM customers"
        ),
        "expected_category": (
            "undefined_column"
        ),
    },
    "table_error": {
        "sql": (
            "SELECT id "
            "FROM customer_accounts"
        ),
        "expected_category": (
            "undefined_table"
        ),
    },
    "join_error": {
        "sql": (
            "SELECT c.name "
            "FROM customers c "
            "JOIN payments p "
            "ON c.id = p.customer_id"
        ),
        "expected_category": (
            "undefined_column"
        ),
    },
}