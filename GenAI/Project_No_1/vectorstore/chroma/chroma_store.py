import chromadb


class ChromaStore:

    def __init__(
        self,
        persist_directory: str = "./vectorstore/chroma",
        collection_name: str = "documents"
    ):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def get_existing_hashes(
        self,
        chunk_hashes: list[str]
    ) -> set[str]:
        """
        Find which chunk hashes already exist in ChromaDB.
        """

        if not chunk_hashes:
            return set()

        result = self.collection.get(
            where={
                "chunk_hash": {
                    "$in": chunk_hashes
                }
            },
            include=["metadatas"]
        )

        existing_hashes = set()

        for metadata in result["metadatas"]:

            if metadata and "chunk_hash" in metadata:
                existing_hashes.add(
                    metadata["chunk_hash"]
                )

        return existing_hashes

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings
    ):
        """
        Store chunks, metadata and embeddings in ChromaDB.
        """

        if not chunks:
            return

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            ids.append(chunk["id"])

            documents.append(
                chunk["text"]
            )

            metadatas.append(
                chunk["metadata"]
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

    def count(self) -> int:
        """
        Return the number of vectors stored in ChromaDB.
        """
        return self.collection.count()