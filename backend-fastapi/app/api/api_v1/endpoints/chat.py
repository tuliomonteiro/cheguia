from fastapi import APIRouter, HTTPException, Depends
from typing import Any
import time

from app.schemas.chat import ChatRequest, ChatResponse, OllamaStatus
from app.services.ollama_service import ollama_service

router = APIRouter()

from app.api import deps
from sqlmodel import Session
from app.services.document_service import document_service

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Chat endpoint using Ollama local LLM with RAG
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    if not ollama_service.is_model_available():
        raise HTTPException(
            status_code=503, 
            detail="Ollama service is not available. Please make sure Ollama is running and the model is installed."
        )
    
    start_time = time.time()
    
    # RAG: Search for relevant documents
    try:
        relevant_docs = await document_service.search_relevant_documents(db, request.message)
    except Exception as e:
        print(f"RAG Error: {e}")
        relevant_docs = []
        
    # Prepare message with context if documents found
    if relevant_docs:
        context_str = "\n\n".join([f"Documento: {doc.title}\n{doc.content}" for doc in relevant_docs])
        # Construct a prompt that includes context
        # We prepend it to the user message so Ollama sees it clearly
        final_message = f"""Usa el siguiente contexto para responder la pregunta, si es relevante:
        
{context_str}

Pregunta del usuario: {request.message}"""
        
        sources = [doc.title for doc in relevant_docs]
    else:
        final_message = request.message
        sources = []

    response = await ollama_service.chat(final_message, request.chat_history)
    processing_time = time.time() - start_time
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
        
    return ChatResponse(
        message=response["message"],
        sources=sources,
        model_used=response.get("model_used"),
        processing_time=processing_time,
        timestamp=time.strftime('%Y-%m-%dT%H:%M:%SZ')
    )

@router.get("/status", response_model=OllamaStatus)
def ollama_status() -> Any:
    """Check Ollama service status and available models"""
    is_available = ollama_service.is_model_available()
    models = ollama_service.get_available_models()
    
    return OllamaStatus(
        status='healthy' if is_available else 'unavailable',
        ollama_available=is_available,
        available_models=models,
        current_model=ollama_service.model
    )
