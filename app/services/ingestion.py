import os
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.config import settings

def load_and_chunk_pdf(file_path: str) -> List[Document]:
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(docs)

    filename = os.path.basename(file_path)
    for i, d in enumerate(chunks):
        d.metadata = d.metadata or {}
        d.metadata["source"] = f"{filename}#chunk_{i}"
        d.metadata["filename"] = filename
        d.metadata["chunk_id"] = i
        d.metadata["path"] = file_path
    return chunks
