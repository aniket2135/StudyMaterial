from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(
        self,
        collection,
        embedding_model: str
    ):
        """
        Initialize the retriever.

        Input:
            collection:
                ChromaDB collection.

            embedding_model:
                Embedding model used during ingestion.
        """

        self.collection = collection

        self.embedding_model = SentenceTransformer(
            embedding_model
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict]:
        """
        Retrieve the most relevant chunks for a query.

        Input:
            query:
                User question.

            top_k:
                Number of chunks to retrieve.

        Output:
            List of relevant chunks with metadata.
        """

        query_embedding = self.embedding_model.encode(
            query,
            normalize_embeddings=True
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        retrieved_chunks = []

        for i, document in enumerate(
            results["documents"][0]
        ):

            retrieved_chunks.append(
                {
                    "text": document,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                }
            )

        return retrieved_chunks