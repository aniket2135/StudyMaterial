from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents: list[dict]) -> list[dict]:
    """
    Split cleaned page-level documents into smaller chunks.

    Input:
        documents:
            List of cleaned PDF pages.

    Output:
        list[dict]:
            List of chunks with text and metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for document in documents:
        page_chunks = splitter.split_text(document["text"])

        for chunk_index, chunk_text in enumerate(page_chunks):

            chunks.append(
                {
                    "text": chunk_text,
                    "metadata": {
                        **document["metadata"],
                        "chunk_index": chunk_index
                    }
                }
            )

    return chunks