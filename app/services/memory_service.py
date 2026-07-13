from collections import defaultdict


conversation_memory = defaultdict(list)


def get_conversation_history(session_id: str) -> list:
    return conversation_memory[session_id]


def add_to_memory(
    session_id: str,
    question: str,
    answer: str,
) -> None:
    conversation_memory[session_id].append(
        {
            "question": question,
            "answer": answer,
        }
    )


def clear_memory(session_id: str) -> None:
    conversation_memory.pop(session_id, None)