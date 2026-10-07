import hashlib

import streamlit as st

from app.ingestion import extract_pdf_pages
from app.chunking import create_chunks
from app.embeddings import create_embeddings
from app.vector_store import clear_collection, add_chunks
from app.retrieval import retrieve_documents
from app.generation import generate_answer
from app.citations import format_citations


st.set_page_config(
    page_title="Financial Document Intelligence",
    page_icon="📄",
    layout="wide",
)


st.title("📄 Financial Document Intelligence")
st.write(
    "Upload a financial PDF and ask questions about it."
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "document_signature" not in st.session_state:
    st.session_state.document_signature = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "page_count" not in st.session_state:
    st.session_state.page_count = 0

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0


# ---------------------------------------------------------
# PDF UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your financial document",
    type=["pdf"],
)


if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    file_signature = hashlib.md5(
        file_bytes
    ).hexdigest()

    # Process only if a new PDF is uploaded
    if (
        st.session_state.document_signature
        != file_signature
    ):

        with st.spinner(
            "Processing your PDF..."
        ):

            # -------------------------------------------------
            # SAVE PDF
            # -------------------------------------------------

            from app.config import RAW_DATA_DIR

            pdf_path = (
                RAW_DATA_DIR /
                uploaded_file.name
            )

            with open(
                pdf_path,
                "wb"
            ) as file:

                file.write(file_bytes)

            # -------------------------------------------------
            # EXTRACT
            # -------------------------------------------------

            pages = extract_pdf_pages(
                pdf_path
            )

            # -------------------------------------------------
            # CHUNK
            # -------------------------------------------------

            chunks = create_chunks(
                pages
            )

            # -------------------------------------------------
            # EMBEDDINGS
            # -------------------------------------------------

            texts = [
                chunk["text"]
                for chunk in chunks
            ]

            embeddings = create_embeddings(
                texts
            )

            # -------------------------------------------------
            # VECTOR DATABASE
            # -------------------------------------------------

            clear_collection()

            add_chunks(
                chunks=chunks,
                embeddings=embeddings,
            )

            # -------------------------------------------------
            # SAVE SESSION INFORMATION
            # -------------------------------------------------

            st.session_state.document_ready = True

            st.session_state.document_signature = (
                file_signature
            )

            st.session_state.document_name = (
                uploaded_file.name
            )

            st.session_state.page_count = (
                len(pages)
            )

            st.session_state.chunk_count = (
                len(chunks)
            )

        st.success(
            "✅ Document processed successfully!"
        )


# ---------------------------------------------------------
# DOCUMENT INFORMATION
# ---------------------------------------------------------

if st.session_state.document_ready:

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Document",
            st.session_state.document_name
        )

    with col2:
        st.metric(
            "Pages",
            st.session_state.page_count
        )

    with col3:
        st.metric(
            "Chunks",
            st.session_state.chunk_count
        )

    st.divider()

    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    st.subheader("💬 Ask a question")

    question = st.text_input(
        "Enter your question",
        placeholder=(
            "Example: What was the company's revenue in 2025?"
        ),
    )

    if st.button(
        "🔍 Ask Question",
        type="primary"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching the document..."
            ):

                retrieved_chunks = (
                    retrieve_documents(
                        question
                    )
                )

            if not retrieved_chunks:

                st.warning(
                    "No relevant information "
                    "was found."
                )

            else:

                with st.spinner(
                    "Generating answer..."
                ):

                    answer = generate_answer(
                        question,
                        retrieved_chunks
                    )

                # ---------------------------------------------
                # ANSWER
                # ---------------------------------------------

                st.subheader("💡 Answer")

                st.write(answer)

                # ---------------------------------------------
                # SOURCES
                # ---------------------------------------------

                st.subheader("📚 Sources")

                citations = format_citations(
                    retrieved_chunks
                )

                for citation in citations:
                    st.write(citation)

                # ---------------------------------------------
                # RETRIEVED EVIDENCE
                # ---------------------------------------------

                with st.expander(
                    "🔎 View retrieved evidence"
                ):

                    for index, chunk in enumerate(
                        retrieved_chunks,
                        start=1
                    ):

                        st.markdown(
                            f"### Source {index}"
                        )

                        st.write(
                            f"**Page:** {chunk['page']}"
                        )

                        st.write(
                            chunk["text"]
                        )

                        st.divider()

else:

    st.info(
        "👆 Upload a PDF to start asking questions."
    )