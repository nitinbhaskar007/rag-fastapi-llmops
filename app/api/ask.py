from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_chain import build_vectorstore, build_rag_chain

router = APIRouter()

class AskBody(BaseModel):
    question: str

@router.post("/ask")
def ask(body: AskBody):
    vs = build_vectorstore()
    chain, _ = build_rag_chain(vs)
    out = chain.invoke({"question": body.question})
    return {"answer": str(out)}
