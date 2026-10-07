from pathlib import Path

from pypdf import PdfReader


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    """
    Extract text from each PDF page while preserving page numbers.
    """

    pdf_path = Path(pdf_path)

    reader = PdfReader(str(pdf_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        text = text.strip()

        if not text:
            continue

        pages.append(
            {
                "page": page_number,
                "text": text,
                "source": pdf_path.name,
            }
        )

    return pages