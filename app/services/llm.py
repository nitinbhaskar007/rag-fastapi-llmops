from langchain_community.chat_models import ChatOllama
from app.core.config import settings

def setup_llm_cache():
    # Optional: you can keep your previous caching logic or skip for local
    return

def build_llm():
    return ChatOllama(
        model=settings.ollama_llm_model,
        base_url=settings.ollama_base_url,
        temperature=0.01,
    )
