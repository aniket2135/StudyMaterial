from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name: str):
        """
        Load the embedding model.

        Input:
            model_name (str):
                Hugging Face embedding model name.

        Example:
            BAAI/bge-small-en-v1.5
        """

        self.model = SentenceTransformer(model_name)

    def generate_embeddings(
        self,
        texts: list[str]
    ):
        """
        Generate embeddings for multiple texts.

        Input:
            texts (list[str]):
                List of chunk texts.

        Output:
            Embeddings corresponding to each text.
        """

        if not texts:
            return []

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )