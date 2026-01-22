import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const { problem, industry, companySize, email } = body

    // Call Python backend API
    try {
      const response = await fetch('http://localhost:8000/api/consult', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          problem, 
          industry, 
          companySize,
          email 
        }),
      })
      
      if (!response.ok) {
        throw new Error(`Backend error: ${response.statusText}`)
      }
      
      const data = await response.json()
      return NextResponse.json(data)
      
    } catch (backendError) {
      console.error('Backend connection error:', backendError)
      // Fall back to mock response if backend is not available
      console.log('Using fallback mock data')
    }

    // Fallback mock response if backend is unavailable
    const mockResponse = {
      recommendations: `Based on your problem in the ${industry} industry, I recommend implementing an AI-powered solution with the following components:

1. **Natural Language Processing (NLP)** for automated text analysis
2. **Machine Learning Models** for pattern recognition and prediction
3. **Retrieval-Augmented Generation (RAG)** for context-aware responses
4. **Automated Classification** for efficient routing

Key Technologies:
- Large Language Models (LLMs) for understanding and generation
- Vector databases for semantic search
- Real-time processing pipeline
- Integration with existing systems

This solution will address your specific challenges while providing scalability and measurable business impact.`,

      businessImpact: {
        cost_savings: `Expected cost reduction of 20-30% through automation. For a ${companySize} company in ${industry}, this typically translates to $15-25K monthly savings by reducing manual processing time and operational overhead.`,
        
        revenue_potential: `Revenue growth potential of 5-10% through improved efficiency and customer satisfaction. Enhanced capabilities can lead to faster service delivery and better customer retention, potentially generating an additional $10-20K monthly.`,
        
        roi_estimate: `Investment: $100-150K for implementation. Expected ROI: 150-200% annually. Break-even point: 6-9 months. First year savings: $180-300K.`,
        
        implementation_timeline: `Total timeline: 4-6 months
- Planning & requirements: 2-4 weeks
- Development & integration: 8-12 weeks  
- Testing & QA: 4-6 weeks
- Deployment & training: 2-4 weeks`,
        
        key_metrics: [
          'Cost per transaction reduction',
          'Processing time improvement', 
          'Customer satisfaction score (CSAT)',
          'First response time (FRT)',
          'Resolution rate',
          'ROI percentage',
          'User adoption rate',
        ],
      },
    }

    // Save consultation request (in production, save to database)
    console.log('Consultation request:', { problem, industry, companySize, email })

    return NextResponse.json(mockResponse)
  } catch (error) {
    console.error('Error processing consultation:', error)
    return NextResponse.json(
      { error: 'Failed to process consultation request' },
      { status: 500 }
    )
  }
}
