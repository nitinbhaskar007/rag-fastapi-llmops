from langchain_community.embeddings import OllamaEmbeddings
from app.core.config import settings

def build_cached_embedder():
    # For Ollama embeddings we don’t need HF endpoints
    return OllamaEmbeddings(
        model=settings.ollama_embed_model,
        base_url=settings.ollama_base_url,
    )
