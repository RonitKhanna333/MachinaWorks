"""
FastAPI web server for AI Consultant chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from chatbot.consultant import AIConsultant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Consultant API",
    description="API for AI/ML/DL/RL consultation and recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize consultant (singleton)
consultant = None


class ConsultationRequest(BaseModel):
    """Request model for consultation"""
    problem: str = Field(..., description="Business problem description")
    context: Optional[str] = Field(None, description="Additional context")
    data_type: Optional[str] = Field(None, description="Type of data involved")
    n_examples: int = Field(5, description="Number of similar examples to retrieve", ge=1, le=10)


class ConsultationResponse(BaseModel):
    """Response model for consultation"""
    problem: str
    recommendations: str
    confidence: str
    similar_cases: List[Dict]


@app.on_event("startup")
async def startup_event():
    """Initialize consultant on startup"""
    global consultant
    logger.info("Initializing AI Consultant...")
    import os
    # Use Groq by default, fallback to others if key not available
    provider = "groq" if os.getenv("GROQ_API_KEY") else ("anthropic" if os.getenv("ANTHROPIC_API_KEY") else "openai")
    consultant = AIConsultant(llm_provider=provider)
    logger.info("✅ AI Consultant ready")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Consultant API",
        "version": "1.0.0",
        "endpoints": {
            "consultation": "/api/consult",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "consultant_ready": consultant is not None
    }


@app.post("/api/consult", response_model=ConsultationResponse)
async def get_consultation(request: ConsultationRequest):
    """
    Get AI/ML/DL/RL consultation for a business problem
    """
    if not consultant:
        raise HTTPException(status_code=503, detail="Consultant not initialized")
    
    try:
        logger.info(f"Processing consultation request: {request.problem}")
        
        result = consultant.suggest(
            problem=request.problem,
            context=request.context,
            data_type=request.data_type,
            n_examples=request.n_examples
        )
        
        return ConsultationResponse(**result)
    
    except Exception as e:
        logger.error(f"Error processing consultation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search_use_cases(query: str, n_results: int = 5):
    """
    Search for similar use cases in the knowledge base
    """
    if not consultant:
        raise HTTPException(status_code=503, detail="Consultant not initialized")
    
    try:
        results = consultant.vector_store.search(query, n_results=n_results)
        return {
            "query": query,
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Error searching use cases: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """
    Get knowledge base statistics
    """
    if not consultant:
        raise HTTPException(status_code=503, detail="Consultant not initialized")
    
    try:
        stats = consultant.vector_store.get_collection_stats()
        return stats
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
