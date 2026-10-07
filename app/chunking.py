from .config import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text: str) -> list[str]:
    """
    Split text into overlapping chunks.
    """

    text = text.strip()

    if len(text) <= CHUNK_SIZE:
        return [text]

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def create_chunks(pages: list[dict]) -> list[dict]:
    """
    Convert PDF pages into chunks while preserving metadata.
    """

    all_chunks = []

    chunk_counter = 1

    for page_data in pages:

        page_number = page_data["page"]
        source = page_data["source"]
        text = page_data["text"]

        page_chunks = split_text(text)

        for chunk_text in page_chunks:

            all_chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_counter}",
                    "text": chunk_text,
                    "page": page_number,
                    "source": source,
                }
            )

            chunk_counter += 1

    return all_chunks