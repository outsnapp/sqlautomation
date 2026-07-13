from typing import Any

from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    session_id: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    sql_query: str | None = None
    raw_result: Any | None = None