import os
import requests


def get_embedder(model: str = "openai/text-embedding-3-small"):
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    def embed_query(text: str):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {"model": model, "input": text}
        response = requests.post(
            "https://openrouter.ai/api/v1/embeddings",
            json=payload,
            headers=headers
        )
        data = response.json()
        return data["data"][0]["embedding"]
    
    def embed_documents(texts: list):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        embeddings = []
        for text in texts:
            payload = {"model": model, "input": text}
            response = requests.post(
                "https://openrouter.ai/api/v1/embeddings",
                json=payload,
                headers=headers
            )
            data = response.json()
            embeddings.append(data["data"][0]["embedding"])
        return embeddings
    
    class EmbedderWrapper:
        def embed_query(self, text: str):
            return embed_query(text)
        
        def embed_documents(self, texts: list):
            return embed_documents(texts)
    
    return EmbedderWrapper()
