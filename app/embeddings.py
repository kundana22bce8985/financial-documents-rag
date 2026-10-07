from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Create embeddings for multiple text chunks.
    """
    if not texts:
        return []

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


def create_query_embedding(query: str) -> list[float]:
    """
    Create an embedding for a user query.
    """
    embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embedding[0].tolist()