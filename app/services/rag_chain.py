from operator import itemgetter
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.passthrough import RunnablePassthrough

from app.services.qdrant_store import get_qdrant_client, ensure_collection
from app.services.embeddings import build_cached_embedder
from app.services.llm import build_llm

_SYSTEM = """You are a helpful assistant.
Use ONLY the provided context to answer.
If the answer is not in the context, say you don't know.
Do not mention that you used context.
"""

_USER = """Question:
{question}

Context:
{context}
"""

def build_vectorstore():
    client = get_qdrant_client()
    ensure_collection(client)
    embedder = build_cached_embedder()

    vs = QdrantVectorStore(
        client=client,
        collection_name=__import__("app.core.config", fromlist=["settings"]).settings.qdrant_collection,
        embedding=embedder,
    )
    return vs

def build_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type=__import__("app.core.config", fromlist=["settings"]).settings.retriever_search_type,
        search_kwargs={"k": __import__("app.core.config", fromlist=["settings"]).settings.retriever_k},
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", _SYSTEM),
        ("human", _USER),
    ])

    llm = build_llm()

    # LCEL: context retrieval runs in parallel with question passthrough
    chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | prompt
        | llm
    )
    return chain, retriever
