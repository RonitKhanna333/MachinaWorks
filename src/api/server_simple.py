"""
Simple FastAPI server - connects frontend to backend AI
Loads AI lazily on first request to avoid startup delays
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="AI Consultancy API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
ai_components = {"initialized": False, "consultant": None, "impact_analyzer": None}


class ConsultRequest(BaseModel):
    problem: str
    industry: str
    companySize: str
    email: str


def init_ai():
    """Initialize AI components lazily"""
    if ai_components["initialized"]:
        return True
    
    try:
        print("\n🤖 Initializing AI components (first request)...")
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from chatbot.consultant import AIConsultant
        from chatbot.impact_analyzer import BusinessImpactAnalyzer
        from embeddings.vector_store import VectorStore
        
        vector_store_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "vectordb")
        vector_store = VectorStore(persist_directory=vector_store_path)
        
        count = vector_store.collection.count()
        print(f"✓ Vector store: {count} embeddings")
        
        if count == 0:
            print("⚠ Vector store empty - run: python quick_start.py")
            return False
        
        ai_components["consultant"] = AIConsultant(vector_store, llm_provider="groq", enable_impact_analysis=True)
        ai_components["impact_analyzer"] = BusinessImpactAnalyzer(llm_provider="groq")
        ai_components["initialized"] = True
        
        print("✅ AI Ready!\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


@app.get("/")
async def health():
    """Health check"""
    return {
        "status": "running",
        "ai_initialized": ai_components["initialized"]
    }


@app.post("/api/consult")
async def consult(request: ConsultRequest):
    """AI Consultation endpoint"""
    
    # Try to initialize AI
    if not ai_components["initialized"]:
        if not init_ai():
            # Return mock data if AI not available
            return {"recommendations": get_mock_text(), "businessImpact": get_mock_impact()}
    
    # Use real AI
    try:
        consultant = ai_components["consultant"]
        result = consultant.suggest(
            problem=request.problem,
            include_impact=True,
            industry=request.industry,
            company_size=request.companySize
        )
        
        # Note: consultant returns "recommendations", not "response"
        response = {"recommendations": result.get("recommendations", ""), "businessImpact": None}
        
        if result.get("business_impact"):
            impact = result["business_impact"]
            
            # Handle both dict and object formats
            if isinstance(impact, dict):
                response["businessImpact"] = {
                    "cost_savings": impact.get("cost_savings", "Analysis not available"),
                    "revenue_potential": impact.get("revenue_potential", "Analysis not available"),
                    "time_savings": impact.get("time_savings", "Analysis not available"),
                    "roi_estimate": impact.get("roi_estimate", "Analysis not available"),
                    "risk_reduction": impact.get("risk_reduction", "Analysis not available"),
                    "competitive_advantage": impact.get("competitive_advantage", "Analysis not available"),
                    "implementation_timeline": impact.get("implementation_timeline", "Analysis not available"),
                    "resource_requirements": impact.get("resource_requirements", "Analysis not available"),
                    "key_metrics": impact.get("key_metrics", []),
                    "success_factors": impact.get("success_factors", []),
                    "potential_challenges": impact.get("potential_challenges", []),
                }
            else:
                # Handle BusinessImpact object
                response["businessImpact"] = {
                    "cost_savings": impact.cost_savings,
                    "revenue_potential": impact.revenue_potential,
                    "time_savings": impact.time_savings,
                    "roi_estimate": impact.roi_estimate,
                    "risk_reduction": impact.risk_reduction,
                    "competitive_advantage": impact.competitive_advantage,
                    "implementation_timeline": impact.implementation_timeline,
                    "resource_requirements": impact.resource_requirements,
                    "key_metrics": impact.key_metrics,
                    "success_factors": impact.success_factors,
                    "potential_challenges": impact.potential_challenges,
                }
        
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"recommendations": get_mock_text(), "businessImpact": get_mock_impact()}


def get_mock_text():
    return "AI system initializing... This is temporary mock data. Please refresh in a moment."


def get_mock_impact():
    return {
        "cost_savings": "Initializing...",
        "revenue_potential": "Initializing...",
        "roi_estimate": "Initializing...",
        "implementation_timeline": "Initializing...",
        "key_metrics": ["Initializing..."]
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 AI Consultancy Backend Starting")
    print("="*60)
    print("\n📍 http://localhost:8000")
    print("📍 http://localhost:8000/docs\n")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
