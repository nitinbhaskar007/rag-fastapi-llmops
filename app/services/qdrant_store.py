from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import settings

def get_qdrant_client() -> QdrantClient:
    mode = settings.qdrant_mode.lower()
    if mode == "memory":
        return QdrantClient(":memory:")
    if mode == "local":
        # local embedded storage
        return QdrantClient(path="./cache/qdrant")
    # url
    return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)

def ensure_collection(client: QdrantClient) -> None:
    name = settings.qdrant_collection
    existing = {c.name for c in client.get_collections().collections}
    if name in existing:
        return
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=settings.embed_dim, distance=Distance.COSINE),
    )
