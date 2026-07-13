from fastapi import APIRouter, HTTPException

from app.schemas import QueryRequest, QueryResponse
from app.services.sql_agent import process_query
from app.services.memory_service import clear_memory


router = APIRouter(
    prefix="/query",
    tags=["SQL Automation"],
)


@router.post("", response_model=QueryResponse)
def query_database(request: QueryRequest):
    try:
        result = process_query(
            question=request.question,
            session_id=request.session_id,
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(error)}",
        )


@router.delete("/memory/{session_id}")
def delete_conversation_memory(session_id: str):
    clear_memory(session_id)

    return {
        "message": "Conversation memory cleared successfully."
    }