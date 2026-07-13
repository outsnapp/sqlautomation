from langchain_openai import ChatOpenAI

from app.config import settings
from app.database import db
from app.prompts.sql_prompts import (
    SQL_GENERATION_PROMPT,
    RESULT_SUMMARY_PROMPT,
)
from app.services.memory_service import (
    get_conversation_history,
    add_to_memory,
)
from app.services.query_validator import validate_query


llm = ChatOpenAI(
    model=settings.MODEL_NAME,
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
    temperature=0,
)


def format_history(history: list) -> str:
    if not history:
        return "No previous conversation."

    formatted_history = ""

    for item in history:
        formatted_history += (
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}\n\n"
        )

    return formatted_history


def clean_sql_query(sql_query: str) -> str:
    sql_query = sql_query.strip()

    if sql_query.startswith("```sql"):
        sql_query = sql_query[6:]

    if sql_query.startswith("```"):
        sql_query = sql_query[3:]

    if sql_query.endswith("```"):
        sql_query = sql_query[:-3]

    return sql_query.strip()


def process_query(question: str, session_id: str) -> dict:
    history = get_conversation_history(session_id)

    schema = db.get_table_info()

    sql_prompt = SQL_GENERATION_PROMPT.format(
        schema=schema,
        history=format_history(history),
        question=question,
    )

    sql_response = llm.invoke(sql_prompt)

    sql_query = clean_sql_query(
        str(sql_response.content)
    )

    if not validate_query(sql_query):
        raise ValueError(
            "Generated SQL query failed the safety validation."
        )

    result = db.run(sql_query)

    summary_prompt = RESULT_SUMMARY_PROMPT.format(
        question=question,
        sql_query=sql_query,
        result=result,
    )

    summary_response = llm.invoke(summary_prompt)

    answer = str(summary_response.content).strip()

    add_to_memory(
        session_id=session_id,
        question=question,
        answer=answer,
    )

    return {
        "question": question,
        "answer": answer,
        "sql_query": sql_query,
        "raw_result": result,
    }