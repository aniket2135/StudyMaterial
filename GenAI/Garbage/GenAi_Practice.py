from ollama import chat

response = chat(
    model="qwen2.5-coder:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain what an API is."
        }
    ]
)

print(response["message"]["content"])

'''
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
'''