import sys
from sqlmodel import Session, select, create_engine
from app.models.document import Document
from app.services.ollama_service import ollama_service
from app.api import deps
from app.core.config import settings
import asyncio
import numpy as np

# Setup DB
engine = create_engine(settings.DATABASE_URI)

def debug_rag():
    with Session(engine) as db:
        # 1. Check documents
        print("Checking documents in DB...")
        docs = db.exec(select(Document)).all()
        print(f"Found {len(docs)} documents.")
        for doc in docs:
            print(f"Doc: {doc.title}, Embedding len: {len(doc.embedding_vector) if doc.embedding_vector else 'None'}")
            
        # 2. Check query embedding
        query = "What is the secret national dish of Paraguay?"
        print(f"\nGenerating embedding for query: '{query}'")
        query_emb = ollama_service.get_embeddings(query)
        print(f"Query embedding len: {len(query_emb)}")
        
        if not docs or not query_emb:
            print("Missing docs or query embedding.")
            return

        # 3. Calculate similarity manually
        print("\nCalculating similarities manually:")
        for doc in docs:
            if not doc.embedding_vector:
                continue
            v1 = np.array(query_emb)
            v2 = np.array(doc.embedding_vector)
            score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            print(f"Doc '{doc.title}' score: {score}")

if __name__ == "__main__":
    debug_rag()
