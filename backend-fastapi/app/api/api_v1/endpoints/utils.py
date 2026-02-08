from fastapi import APIRouter
from typing import Any

router = APIRouter()

@router.get("/health")
def health_check() -> Any:
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "message": "Paraguay Guide API is running",
        "version": "1.0.0"
    }
