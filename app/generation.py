from google import genai

from .config import GEMINI_API_KEY, GEMINI_LLM_MODEL


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it to your .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(
    question: str,
    retrieved_chunks: list[dict]
) -> str:

    if not retrieved_chunks:
        return (
            "I could not find relevant information "
            "in the uploaded document."
        )

    context_parts = []

    for index, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {index}
Document: {chunk['source']}
Page: {chunk['page']}
Chunk ID: {chunk['chunk_id']}

Content:
{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are a financial document question-answering assistant.

Answer the user's question ONLY using the provided document
evidence.

Do not use outside knowledge.

If the answer is not present in the evidence, clearly say:
"I could not find the answer in the uploaded document."

Give a concise and accurate answer.

When useful, mention the relevant page number.

DOCUMENT EVIDENCE:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model=GEMINI_LLM_MODEL,
        contents=prompt,
    )

    return response.text