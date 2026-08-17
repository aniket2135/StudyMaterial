from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: Path) -> list[dict]:
    """
    Extract text from a PDF while preserving page-level metadata.
    """

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        documents.append(
            {
                "text": text,
                "metadata": {
                    "source": pdf_path.name,
                    "page_number": page_number,
                    "file_path": str(pdf_path),
                },
            }
        )

    return documents



'''

data/raw/document.pdf
        ↓
   pdf_loader.py
        ↓
┌─────────────────────────┐
│ Page 1                  │
│ text: ...               │
│ source: document.pdf    │
│ page: 1                 │
├─────────────────────────┤
│ Page 2                  │
│ text: ...               │
│ source: document.pdf    │
│ page: 2                 │
└─────────────────────────┘

'''