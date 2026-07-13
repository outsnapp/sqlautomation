import re


BLOCKED_KEYWORDS = {
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "GRANT",
    "REVOKE",
}


def validate_query(sql_query: str) -> bool:
    if not sql_query or not sql_query.strip():
        return False

    normalized_query = remove_sql_comments(sql_query).upper()

    for keyword in BLOCKED_KEYWORDS:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, normalized_query):
            return False

    if not normalized_query.strip().startswith("SELECT"):
        return False

    return True


def remove_sql_comments(sql_query: str) -> str:
    sql_query = re.sub(
        r"--.*?$",
        "",
        sql_query,
        flags=re.MULTILINE,
    )

    sql_query = re.sub(
        r"/\*.*?\*/",
        "",
        sql_query,
        flags=re.DOTALL,
    )

    return sql_query