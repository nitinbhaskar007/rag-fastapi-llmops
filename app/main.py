import os
from fastapi import FastAPI
from app.core.logging import setup_logging
from app.services.llm import setup_llm_cache

from app.api.health import router as health_router
from app.api.ingest import router as ingest_router
from app.api.ask import router as ask_router
from app.api.eval import router as eval_router

def create_app() -> FastAPI:
    setup_logging()
    setup_llm_cache()

    # Ensure directories exist
    os.makedirs("./cache", exist_ok=True)
    os.makedirs("./data/uploads", exist_ok=True)
    os.makedirs("./data/golden", exist_ok=True)

    app = FastAPI(title="RAG FastAPI LLMOps")

    app.include_router(health_router)
    app.include_router(ingest_router, tags=["ingestion"])
    app.include_router(ask_router, tags=["rag"])
    app.include_router(eval_router, tags=["eval"])

    return app

app = create_app()
