from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    message: str
    sources: List[str] = []
    model_used: Optional[str] = None
    processing_time: Optional[float] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None

class OllamaStatus(BaseModel):
    status: str
    ollama_available: bool
    current_model: str
    available_models: List[str]
