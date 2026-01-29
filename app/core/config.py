from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # HF
    llm_provider: str = Field(default="ollama", alias="LLM_PROVIDER")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_llm_model: str = Field(default="llama3.1:8b", alias="OLLAMA_LLM_MODEL")
    ollama_embed_model: str = Field(default="nomic-embed-text", alias="OLLAMA_EMBED_MODEL")


    # Qdrant
    qdrant_mode: str = Field(default="url", alias="QDRANT_MODE")  # url|local|memory
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_collection: str = Field(default="rag_docs", alias="QDRANT_COLLECTION")
    qdrant_api_key: str = Field(default="", alias="QDRANT_API_KEY")

    # RAG settings
    embed_dim: int = Field(default=768, alias="EMBED_DIM")
    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=100, alias="CHUNK_OVERLAP")
    retriever_search_type: str = Field(default="mmr", alias="RETRIEVER_SEARCH_TYPE")
    retriever_k: int = Field(default=4, alias="RETRIEVER_K")

    # Caches
    embed_cache_dir: str = Field(default="./cache/embeddings", alias="EMBED_CACHE_DIR")
    llm_cache: str = Field(default="memory", alias="LLM_CACHE")  # memory|sqlite
    sqlite_cache_path: str = Field(default="./cache/llm_cache.sqlite", alias="SQLITE_CACHE_PATH")

    # LangSmith
    langchain_tracing_v2: str = Field(default="false", alias="LANGCHAIN_TRACING_V2")
    langchain_project: str = Field(default="rag-fastapi-llmops", alias="LANGCHAIN_PROJECT")
    langchain_api_key: str = Field(default="", alias="LANGCHAIN_API_KEY")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
