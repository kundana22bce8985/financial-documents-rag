import chromadb

from .config import VECTOR_STORE_DIR


client = chromadb.PersistentClient(
    path=str(VECTOR_STORE_DIR)
)


COLLECTION_NAME = "financial_documents"


def get_collection():
    """
    Get the Chroma collection.
    """

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def clear_collection():
    """
    Delete the existing collection.
    """

    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )
    except Exception:
        pass


def add_chunks(
    chunks: list[dict],
    embeddings: list[list[float]]
):
    """
    Store chunks and their embeddings in ChromaDB.
    """

    collection = get_collection()

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(chunk["chunk_id"])

        documents.append(chunk["text"])

        metadatas.append(
            {
                "page": chunk["page"],
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search(
    query_embedding: list[float],
    top_k: int = 5
) -> list[dict]:

    collection = get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_chunks.append(
            {
                "text": document,
                "page": metadata["page"],
                "source": metadata["source"],
                "chunk_id": metadata["chunk_id"],
                "distance": distance,
            }
        )

    return retrieved_chunks