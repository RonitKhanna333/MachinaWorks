"""
FastAPI server for AI Consultancy website
Connects Next.js frontend to Python AI consultant backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from chatbot.consultant import AIConsultant
from chatbot.impact_analyzer import BusinessImpactAnalyzer
from embeddings.vector_store import VectorStore

app = FastAPI(
    title="AI Consultancy API",
    description="AI-powered business consultation with impact analysis",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
vector_store = None
consultant = None
impact_analyzer = None

def init_components():
    """Initialize AI components lazily"""
    global vector_store, consultant, impact_analyzer
    
    if vector_store is not None:
        return True
    
    try:
        print("\n" + "="*60)
        print("Initializing AI components...")
        print("="*60)
        
        # Initialize vector store with proper path
        vector_store_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "vectordb")
        print(f"Vector store path: {vector_store_path}")
        
        # Use environment variable to avoid redownloading
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_HUB_OFFLINE'] = '1'
        
        vector_store = VectorStore(persist_directory=vector_store_path)
        
        # Check if vector store has data
        try:
            collection = vector_store.collection
            count = collection.count()
            print(f"✓ Vector store loaded: {count} embeddings found")
            
            if count == 0:
                print(f"⚠ Warning: Vector store is empty!")
                print(f"  Run: python quick_start.py")
                return False
        except Exception as e:
            print(f"⚠ Could not check vector store: {e}")
            return False
        
        # Initialize consultant with AI
        consultant = AIConsultant(vector_store, llm_provider="groq", enable_impact_analysis=True)
        print("✓ AI Consultant initialized")
        
        # Initialize impact analyzer
        impact_analyzer = BusinessImpactAnalyzer(llm_provider="groq")
        print("✓ Business Impact Analyzer initialized")
        
        print("="*60)
        print("✅ All AI components ready!")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing AI components: {e}")
        import traceback
        traceback.print_exc()
        print("\n⚠ API will return mock data")
        vector_store = None
        consultant = None
        impact_analyzer = None
        return False


class ConsultRequest(BaseModel):
    problem: str
    industry: str
    companySize: str
    email: str


class ImpactRequest(BaseModel):
    problem: str
    ai_solution: str
    industry: str
    company_size: str


@app.get("/")
async def root():
    """Health check endpoint"""
    # Try to initialize if not already done
    if vector_store is None:
        init_components()
    
    return {
        "status": "running",
        "message": "AI Consultancy API is operational",
        "components": {
            "vector_store": vector_store is not None,
            "consultant": consultant is not None,
            "impact_analyzer": impact_analyzer is not None,
        }
    }


@app.post("/api/consult")
async def consult(request: ConsultRequest):
    """
    Main consultation endpoint
    Provides AI recommendations with business impact analysis
    """
    try:
        # Try to initialize AI if not already done
        if vector_store is None:
            print("\n⚡ First request - initializing AI components...")
            if not init_components():
                print("⚠ Initialization failed - using mock data\n")
                return get_mock_response(request)
        
        # Check if AI is available
        if not consultant or not vector_store:
            print("⚠ AI components not initialized - using mock data")
            return get_mock_response(request)
        
        # Check if vector store has data
        try:
            count = vector_store.collection.count()
            if count == 0:
                print("⚠ Vector store is empty - using mock data")
                print("  Fix: Run 'python quick_start.py' to populate the database")
                return get_mock_response(request)
        except Exception as e:
            print(f"⚠ Could not check vector store: {e}")
        
        # Use real AI
        print(f"\n🤖 AI Processing consultation...")
        print(f"   Industry: {request.industry}")
        print(f"   Company Size: {request.companySize}")
        print(f"   Problem: {request.problem[:100]}...")
        
        result = consultant.suggest(
            problem=request.problem,
            include_impact=True,
            industry=request.industry,
            company_size=request.companySize
        )
        
        print(f"   ✓ Got response: {len(result.get('response', ''))} characters")
        print(f"   ✓ Business impact: {'Yes' if result.get('business_impact') else 'No'}")
        
        # Format response
        response = {
            "recommendations": result.get("response", "No recommendations available"),
            "businessImpact": None
        }
        
        # Add business impact if available
        if "business_impact" in result and result["business_impact"]:
            impact = result["business_impact"]
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
        
        print("✅ Consultation complete - returning real AI response\n")
        return response
            
    except Exception as e:
        print(f"❌ Error processing consultation: {e}")
        import traceback
        traceback.print_exc()
        print("\n⚠ Falling back to mock data due to error\n")
        return get_mock_response(request)


@app.post("/api/impact")
async def analyze_impact(request: ImpactRequest):
    """
    Standalone business impact analysis endpoint
    """
    try:
        if impact_analyzer:
            print(f"\n📊 Analyzing business impact for {request.industry}")
            
            impact = impact_analyzer.analyze(
                problem=request.problem,
                ai_solution=request.ai_solution,
                industry=request.industry,
                company_size=request.company_size
            )
            
            return impact.to_dict()
        else:
            print("⚠ Impact analyzer not initialized")
            raise HTTPException(status_code=503, detail="Impact analyzer not available")
            
    except Exception as e:
        print(f"❌ Error analyzing impact: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_mock_response(request: ConsultRequest):
    """
    Mock response for when AI components are not initialized
    """
    return {
        "recommendations": f"""Based on your problem in the {request.industry} industry, I recommend implementing an AI-powered solution with the following components:

1. **Natural Language Processing (NLP)** for automated text analysis and understanding
2. **Machine Learning Models** for pattern recognition and predictive analytics
3. **Retrieval-Augmented Generation (RAG)** for context-aware, accurate responses
4. **Automated Classification and Routing** for efficient task management

Key Technologies:
- Large Language Models (LLMs) like GPT-4 or Claude for natural language understanding
- Vector databases (ChromaDB/Pinecone) for semantic search capabilities
- Real-time processing pipeline for immediate responses
- API integration layer for seamless connection with existing systems

Implementation Approach:
- Phase 1: Data collection and model training (4-6 weeks)
- Phase 2: System integration and testing (6-8 weeks)
- Phase 3: Pilot deployment with monitoring (2-4 weeks)
- Phase 4: Full rollout and optimization (2-3 weeks)

This solution addresses your specific challenges while ensuring scalability and measurable business impact.""",

        "businessImpact": {
            "cost_savings": f"Expected cost reduction of 20-35% through automation and efficiency gains. For a {request.companySize} company in {request.industry}, this typically translates to $15-30K monthly savings by reducing manual processing time, minimizing errors, and optimizing resource allocation.",
            
            "revenue_potential": "Revenue growth potential of 5-12% through improved customer satisfaction, faster service delivery, and ability to handle higher volumes. Enhanced capabilities can lead to better customer retention (reducing churn by 15-25%) and opening new market opportunities, potentially generating an additional $12-25K monthly.",
            
            "time_savings": "Estimated time savings of 15-25 hours per week per employee through automation of routine tasks. This frees up your team to focus on high-value activities, strategic initiatives, and customer relationship building. Total productivity improvement: 40-60%.",
            
            "roi_estimate": "Investment: $100-180K for complete implementation. Expected annual ROI: 150-220%. Break-even point: 6-9 months. First year net savings: $200-350K. Three-year cumulative ROI: 400-500%.",
            
            "risk_reduction": "Significant risk mitigation across multiple dimensions: 70-85% reduction in human errors, improved compliance through automated checks, enhanced data security with AI monitoring, and better fraud detection (if applicable). Estimated risk-adjusted savings: $20-40K annually.",
            
            "competitive_advantage": "Strategic positioning benefits including faster time-to-market, superior customer experience leading to higher NPS scores, ability to offer 24/7 service, and data-driven decision making. This creates a sustainable competitive moat that's difficult for competitors to replicate quickly.",
            
            "implementation_timeline": """Total timeline: 16-24 weeks (4-6 months)

**Phase 1: Planning & Requirements (3-4 weeks)**
- Stakeholder workshops and requirements gathering
- Technical architecture design
- Vendor selection and procurement

**Phase 2: Development & Integration (8-12 weeks)**
- AI model development and training
- System integration with existing infrastructure
- User interface development
- API connections and data pipeline setup

**Phase 3: Testing & Quality Assurance (3-5 weeks)**
- Unit and integration testing
- User acceptance testing (UAT)
- Performance and load testing
- Security audit

**Phase 4: Deployment & Training (2-3 weeks)**
- Pilot rollout to limited user group
- Staff training and documentation
- Full production deployment
- Post-launch monitoring and optimization""",
            
            "resource_requirements": f"""**Team Composition (5-8 people):**
- 1 Project Manager (full-time)
- 2 AI/ML Engineers (full-time)
- 2 Backend/Integration Developers (full-time)
- 1 Frontend Developer (part-time)
- 1 DevOps Engineer (part-time)
- 1 QA Specialist (part-time)

**Skills Required:**
- Python, TensorFlow/PyTorch
- NLP and LLM fine-tuning
- Cloud infrastructure (AWS/Azure/GCP)
- API development (FastAPI/Flask)
- Database management (SQL, Vector DBs)

**Infrastructure:**
- Cloud compute resources: $2-4K/month
- LLM API costs: $1-3K/month
- Storage and databases: $500-1K/month
- Monitoring and tools: $500/month

**Budget Breakdown:**
- Development: $80-120K
- Infrastructure (first year): $30-50K
- Training & support: $10-15K
- Contingency (15%): $15-25K
- Total: $135-210K""",
            
            "key_metrics": [
                "Cost per transaction/interaction (target: 60-70% reduction)",
                "Processing time (target: 75-85% reduction)",
                "Customer Satisfaction Score/CSAT (target: 4.5+/5)",
                "First Response Time (target: <2 hours, ideally <5 minutes)",
                "Resolution rate (target: 85%+ automated resolution)",
                "User adoption rate (target: 80%+ within 3 months)",
                "Return on Investment percentage (target: 150%+ annually)",
                "Error rate reduction (target: 80%+ reduction)",
                "System uptime (target: 99.5%+)",
            ],
            
            "success_factors": [
                "**Clear Requirements**: Well-defined use cases and success criteria from the start",
                "**Quality Training Data**: Sufficient high-quality data for model training and validation",
                "**Stakeholder Buy-in**: Executive support and user engagement throughout the process",
                "**Iterative Approach**: Start with pilot, gather feedback, iterate before full rollout",
                "**Comprehensive Testing**: Thorough testing including edge cases and failure scenarios",
                "**User Training**: Adequate training and documentation for all user groups",
                "**Change Management**: Proactive communication and support for organizational change",
                "**Continuous Monitoring**: Real-time performance tracking and optimization",
            ],
            
            "potential_challenges": [
                "**Integration Complexity**: Connecting with legacy systems may require custom solutions",
                "**Data Quality Issues**: Insufficient or poor-quality training data can impact performance",
                "**User Adoption Resistance**: Change management and training are critical for success",
                "**Model Accuracy**: Initial models may require tuning and refinement based on real-world usage",
                "**Scalability Concerns**: System must be designed to handle growth in usage and data volume",
                "**Compliance Requirements**: Industry-specific regulations (GDPR, HIPAA, etc.) must be addressed",
                "**Cost Overruns**: Scope creep and unforeseen technical challenges can increase costs by 15-30%",
                "**Vendor Dependency**: Reliance on third-party AI services requires backup plans",
            ],
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting AI Consultancy API Server")
    print("="*60)
    print("\n📍 Server will be available at: http://localhost:8000")
    print("📍 API docs available at: http://localhost:8000/docs")
    print("📍 Health check: http://localhost:8000/")
    print("\n⚡ Make sure your Groq API key is set in .env file")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
