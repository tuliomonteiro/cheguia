from typing import List, Optional
from sqlmodel import Session, select
from app.models.document import Document
from app.services.ollama_service import ollama_service
import numpy as np

class DocumentService:
    def __init__(self):
        pass

    async def create_document(self, db: Session, title: str, content: str, document_type: str, source_url: Optional[str] = None):
        """Create a new document and generate its embedding"""
        
        # Generate embedding
        embedding = ollama_service.get_embeddings(content)
        
        db_document = Document(
            title=title,
            content=content,
            document_type=document_type,
            source_url=source_url,
            embedding_vector=embedding
        )
        
        db.add(db_document)
        await db.commit()
        await db.refresh(db_document)
        return db_document

    def split_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Split text into chunks with overlap"""
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
            
        return chunks

    async def ingest_document(self, db: Session, title: str, content: str, document_type: str, source_url: Optional[str] = None) -> List[Document]:
        """Ingest a document, chunking it if necessary"""
        chunks = self.split_text(content)
        created_docs = []
        
        for i, chunk in enumerate(chunks):
            chunk_title = f"{title} (Part {i+1})"
            try:
                doc = await self.create_document(db, chunk_title, chunk, document_type, source_url)
                if doc.embedding_vector:
                    created_docs.append(doc)
            except Exception as e:
                print(f"Error creating chunk {i+1}: {e}")
                
        return created_docs

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if not v1 or not v2:
            return 0.0
        
        a = np.array(v1)
        b = np.array(v2)
        
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return np.dot(a, b) / (norm_a * norm_b)

    async def search_relevant_documents(self, db: Session, query: str, k: int = 3) -> List[Document]:
        """Search for relevant documents using vector similarity"""
        
        # 1. Generate query embedding
        query_embedding = ollama_service.get_embeddings(query)
        if not query_embedding:
            return []
            
        # 2. Fetch all documents with embeddings
        # In a production w/ pgvector, we would do this in SQL
        statement = select(Document).where(Document.embedding_vector != None)
        result = await db.execute(statement)
        documents = result.scalars().all()
        
        if not documents:
            return []
            
        # 3. Calculate similarity
        scored_docs = []
        for doc in documents:
            if not doc.embedding_vector:
                continue
                
            # Ensure vector is list of floats
            try:
                # If stored as JSON, it might be a list already
                doc_vector = doc.embedding_vector
                score = self.cosine_similarity(query_embedding, doc_vector)
                scored_docs.append((score, doc))
            except Exception as e:
                print(f"Error calculating similarity for doc {doc.id}: {e}")
                continue
        
        # 4. Sort and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Filter by threshold if needed (e.g. > 0.5)
        return [doc for score, doc in scored_docs[:k]]

document_service = DocumentService()
