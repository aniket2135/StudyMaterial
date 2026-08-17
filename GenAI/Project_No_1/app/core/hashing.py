import hashlib


def generate_chunk_hash(text: str) -> str:
    """
    Generate a deterministic SHA-256 hash for a chunk.

    Input:
        text (str):
            Chunk text.

    Output:
        str:
            SHA-256 hexadecimal hash.
    """

    normalized_text = text.strip()

    return hashlib.sha256(
        normalized_text.encode("utf-8")
    ).hexdigest()