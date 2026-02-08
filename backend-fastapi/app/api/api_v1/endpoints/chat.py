from fastapi import APIRouter, HTTPException, Depends
from typing import Any
import time

from app.schemas.chat import ChatRequest, ChatResponse, OllamaStatus
from app.services.ollama_service import ollama_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> Any:
    """
    Chat endpoint using Ollama local LLM
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    if not ollama_service.is_model_available():
        raise HTTPException(
            status_code=503, 
            detail="Ollama service is not available. Please make sure Ollama is running and the model is installed."
        )
    
    start_time = time.time()
    response = await ollama_service.chat(request.message, request.chat_history)
    processing_time = time.time() - start_time
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
        
    return ChatResponse(
        message=response["message"],
        sources=response.get("sources", []),
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
