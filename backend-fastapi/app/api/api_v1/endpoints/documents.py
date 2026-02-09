from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from sqlmodel import Session
from typing import Any, List
from pydantic import BaseModel
import fitz  # PyMuPDF

from app.api import deps
from app.services.document_service import document_service
from app.models.document import Document

router = APIRouter()

class DocumentCreate(BaseModel):
    title: str
    content: str
    document_type: str = "article"
    source_url: str = None

@router.post("/upload-pdf", response_model=Document)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Upload a PDF file, extract text, and create a document with embeddings.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Read file content
        content = await file.read()
        
        # Open PDF with PyMuPDF
        with fitz.open(stream=content, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
                
        if not text.strip():
             raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        # Ingest document (chunks)
        docs = await document_service.ingest_document(
            db=db,
            title=file.filename,
            content=text,
            document_type="pdf",
            source_url=f"upload://{file.filename}"
        )
        
        if not docs:
            raise HTTPException(status_code=500, detail="Failed to create document chunks or embeddings")
            
        # Return the first one as representative, or modify response to list
        # For this endpoint, returning the first one is enough to correct the type error
        return docs[0]
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@router.post("/", response_model=Document)
async def create_document(
    doc_in: DocumentCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create a new document and generate embeddings for RAG.
    """
    try:
        doc = await document_service.create_document(
            db=db,
            title=doc_in.title,
            content=doc_in.content,
            document_type=doc_in.document_type,
            source_url=doc_in.source_url
        )
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create document: {str(e)}")
