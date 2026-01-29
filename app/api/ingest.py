import os
from fastapi import APIRouter, UploadFile, File
from app.services.ingestion import load_and_chunk_pdf
from app.services.rag_chain import build_vectorstore

router = APIRouter()

UPLOAD_DIR = "./data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())

    chunks = load_and_chunk_pdf(path)
    vs = build_vectorstore()
    ids = vs.add_documents(chunks)

    return {"ok": True, "file": file.filename, "chunks": len(chunks), "ids_added": len(ids)}
