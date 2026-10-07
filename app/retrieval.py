from .config import TOP_K_RETRIEVAL
from .embeddings import create_query_embedding
from .vector_store import search


def retrieve_documents(
    question: str,
    top_k: int = TOP_K_RETRIEVAL
) -> list[dict]:
    """
    Retrieve the most relevant document chunks
    for the user's question.
    """

    query_embedding = create_query_embedding(question)

    results = search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    return results