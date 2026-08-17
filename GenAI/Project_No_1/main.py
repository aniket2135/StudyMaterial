from configs.settings import (
    PDF_DIRECTORY,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    CHROMA_COLLECTION,
)

from ingestion.loaders.pdf_loader import load_pdf

from ingestion.preprocessing.header_footer_remover import (
    detect_headers_and_footers,
    remove_headers_and_footers,
)

from ingestion.preprocessing.text_cleaner import (
    clean_text
)

from ingestion.chunking.text_chunker import (
    create_chunks
)

from app.core.hashing import (
    generate_chunk_hash
)

from app.embeddings.embedding_service import (
    EmbeddingService
)

from vectorstore.chroma.chroma_store import (
    ChromaStore
)

def main():

    # ============================================================
    # STEP 1
    # Find PDF
    # ============================================================

    pdf_files = [PDF_DIRECTORY]

    if not pdf_files:

        print(
            f"No PDF files found: {PDF_DIRECTORY}"
        )

        return

    # ============================================================
    # Initialize embedding service
    # ============================================================

    print("\nLoading embedding model...")

    embedding_service = EmbeddingService(
        EMBEDDING_MODEL
    )

    print(
        f"Embedding model loaded: "
        f"{EMBEDDING_MODEL}"
    )

    # ============================================================
    # Initialize ChromaDB
    # ============================================================

    chroma_store = ChromaStore(
        persist_directory=str(CHROMA_PATH),
        collection_name=CHROMA_COLLECTION
    )

    print(
        f"ChromaDB collection: "
        f"{CHROMA_COLLECTION}"
    )

    # ============================================================
    # Process PDFs
    # ============================================================

    for pdf_path in pdf_files:

        print("\n" + "=" * 70)
        print(
            f"Processing PDF: {pdf_path.name}"
        )
        print("=" * 70)

        # ========================================================
        # STEP 2
        # Load PDF
        # ========================================================

        documents = load_pdf(
            pdf_path
        )

        print(
            f"Pages extracted: "
            f"{len(documents)}"
        )

        # ========================================================
        # STEP 3
        # Detect headers and footers
        # ========================================================

        headers, footers = (
            detect_headers_and_footers(
                documents
            )
        )

        print(
            f"Headers detected: "
            f"{len(headers)}"
        )

        print(
            f"Footers detected: "
            f"{len(footers)}"
        )

        # ========================================================
        # STEP 4
        # Remove headers and footers
        # ========================================================

        documents = (
            remove_headers_and_footers(
                documents,
                headers,
                footers
            )
        )

        print(
            "Headers and footers removed."
        )

        # ========================================================
        # STEP 5
        # Clean text
        # ========================================================

        for document in documents:

            document["text"] = (
                clean_text(
                    document["text"]
                )
            )

        print(
            "Text cleaning completed."
        )

        # ========================================================
        # STEP 6
        # Create chunks
        # ========================================================

        chunks = create_chunks(
            documents
        )

        print(
            f"Total chunks created: "
            f"{len(chunks)}"
        )

        # ========================================================
        # STEP 7
        # Generate hash for every chunk
        # ========================================================

        for chunk in chunks:

            chunk_hash = (
                generate_chunk_hash(
                    chunk["text"]
                )
            )

            # Use hash as unique ID
            chunk["id"] = chunk_hash

            # Store hash in metadata
            chunk["metadata"][
                "chunk_hash"
            ] = chunk_hash

        print(
            "Chunk hashes generated."
        )

        # ========================================================
        # STEP 8
        # Remove duplicate chunks
        # within current ingestion
        # ========================================================

        unique_chunks = []
        seen_hashes = set()

        for chunk in chunks:

            chunk_hash = (
                chunk["metadata"][
                    "chunk_hash"
                ]
            )

            if chunk_hash in seen_hashes:
                continue

            seen_hashes.add(
                chunk_hash
            )

            unique_chunks.append(
                chunk
            )

        chunks = unique_chunks

        print(
            f"Unique chunks: "
            f"{len(chunks)}"
        )

        # ========================================================
        # STEP 9
        # Check ChromaDB
        # ========================================================

        chunk_hashes = [
            chunk["metadata"][
                "chunk_hash"
            ]
            for chunk in chunks
        ]

        existing_hashes = (
            chroma_store.get_existing_hashes(
                chunk_hashes
            )
        )

        print(
            f"Already embedded: "
            f"{len(existing_hashes)}"
        )

        # ========================================================
        # STEP 10
        # Keep only new chunks
        # ========================================================

        new_chunks = [
            chunk
            for chunk in chunks
            if chunk["metadata"][
                "chunk_hash"
            ] not in existing_hashes
        ]

        print(
            f"New chunks: "
            f"{len(new_chunks)}"
        )

        # ========================================================
        # STEP 11
        # Generate embeddings
        # ========================================================

        if not new_chunks:

            print(
                "No new chunks."
            )

            print(
                "Embedding skipped."
            )

            continue

        print(
            "\nGenerating embeddings..."
        )

        texts = [
            chunk["text"]
            for chunk in new_chunks
        ]

        embeddings = (
            embedding_service
            .generate_embeddings(
                texts
            )
        )

        print(
            "Embeddings generated."
        )

        # ========================================================
        # STEP 12
        # Store in ChromaDB
        # ========================================================

        chroma_store.add_chunks(
            new_chunks,
            embeddings
        )

        print(
            f"Stored {len(new_chunks)} "
            f"new chunks in ChromaDB."
        )

    # ============================================================
    # Final status
    # ============================================================

    print("\n" + "=" * 70)

    print(
        f"Total vectors in ChromaDB: "
        f"{chroma_store.count()}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()