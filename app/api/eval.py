from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.eval_ragas import run_ragas_eval
from app.services.rag_chain import build_vectorstore, build_rag_chain

router = APIRouter()

class EvalItem(BaseModel):
    question: str
    ground_truth: Optional[str] = None

class EvalBody(BaseModel):
    items: List[EvalItem]

@router.post("/eval/run")
def eval_run(body: EvalBody):
    vs = build_vectorstore()
    chain, retriever = build_rag_chain(vs)

    samples = []
    for item in body.items:
        docs = retriever.invoke(item.question)
        contexts = [d.page_content for d in docs]
        answer = str(chain.invoke({"question": item.question}))
        samples.append({
            "question": item.question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": item.ground_truth or "",
        })

    return run_ragas_eval(samples)
