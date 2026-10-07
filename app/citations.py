def format_citations(
    retrieved_chunks: list[dict]
) -> list[str]:

    citations = []

    seen = set()

    for chunk in retrieved_chunks:

        key = (
            chunk["source"],
            chunk["page"]
        )

        if key in seen:
            continue

        seen.add(key)

        citations.append(
            f"📄 {chunk['source']} — Page {chunk['page']}"
        )

    return citations