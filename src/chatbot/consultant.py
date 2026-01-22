"""
AI Consultant Chatbot with RAG
Provides AI/ML/DL/RL recommendations based on business problems
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from typing import List, Dict, Optional
import logging

from embeddings.vector_store import VectorStore
from chatbot.impact_analyzer import BusinessImpactAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIConsultant:
    """
    AI Consultation chatbot that suggests appropriate AI/ML/DL/RL techniques
    based on business problems using RAG (Retrieval Augmented Generation)
    """
    
    def __init__(
        self, 
        vector_store: Optional[VectorStore] = None,
        llm_provider: str = "groq",  # or "anthropic", "openai"
        enable_impact_analysis: bool = True
    ):
        """
        Initialize AI Consultant
        
        Args:
            vector_store: Pre-initialized vector store (creates new if None)
            llm_provider: LLM provider to use ('groq', 'anthropic', or 'openai')
            enable_impact_analysis: Whether to enable business impact analysis
        """
        self.vector_store = vector_store or VectorStore()
        self.llm_provider = llm_provider
        self.enable_impact_analysis = enable_impact_analysis
        
        # Initialize LLM client
        if llm_provider == "groq":
            from groq import Groq
            import os
            self.llm_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model = "llama-3.3-70b-versatile"  # Fast and powerful
        elif llm_provider == "anthropic":
            from anthropic import Anthropic
            import os
            self.llm_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-5-sonnet-20241022"
        elif llm_provider == "openai":
            from openai import OpenAI
            import os
            self.llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-4-turbo-preview"
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        # Initialize business impact analyzer
        if self.enable_impact_analysis:
            try:
                self.impact_analyzer = BusinessImpactAnalyzer(llm_provider=llm_provider)
                logger.info("✅ Business Impact Analyzer enabled")
            except Exception as e:
                logger.warning(f"Could not initialize impact analyzer: {e}")
                self.impact_analyzer = None
        else:
            self.impact_analyzer = None
        
        logger.info(f"AI Consultant initialized with {llm_provider} ({self.model})")
    
    def suggest(
        self, 
        problem: str, 
        context: Optional[str] = None,
        data_type: Optional[str] = None,
        n_examples: int = 5,
        include_impact: bool = True,
        industry: Optional[str] = None,
        company_size: Optional[str] = None
    ) -> Dict:
        """
        Suggest AI/ML/DL/RL techniques for a business problem
        
        Args:
            problem: Business problem description
            context: Additional context (industry, scale, constraints)
            data_type: Type of data involved (optional filter)
            n_examples: Number of similar examples to retrieve
            include_impact: Whether to include business impact analysis
            industry: Industry context for impact analysis
            company_size: Company size for impact analysis
        
        Returns:
            Dict with recommendations, reasoning, and optional impact analysis
        """
        logger.info(f"Processing suggestion request for: {problem}")
        
        # Step 1: Retrieve similar use cases
        similar_cases = self.vector_store.search(
            query=problem,
            n_results=n_examples
        )
        
        # Step 2: Build context from retrieved examples
        retrieved_context = self._format_retrieved_context(similar_cases)
        
        # Step 3: Create prompt for LLM
        prompt = self._create_consultation_prompt(
            problem=problem,
            context=context,
            retrieved_cases=retrieved_context
        )
        
        # Step 4: Get LLM response
        response = self._query_llm(prompt)
        
        # Step 5: Add business impact analysis
        impact_analysis = None
        if include_impact and self.impact_analyzer:
            try:
                logger.info("Generating business impact analysis...")
                impact_obj = self.impact_analyzer.analyze(
                    problem=problem,
                    ai_solution=response,
                    industry=industry,
                    company_size=company_size
                )
                impact_analysis = impact_obj.to_dict()
            except Exception as e:
                logger.warning(f"Could not generate impact analysis: {e}")
        
        # Step 6: Format final response
        result = {
            'problem': problem,
            'recommendations': response,
            'similar_cases': similar_cases,
            'confidence': self._calculate_confidence(similar_cases)
        }
        
        if impact_analysis:
            result['business_impact'] = impact_analysis
        
        return result
    
    def _format_retrieved_context(self, similar_cases: List[Dict]) -> str:
        """Format retrieved use cases into context string"""
        
        context_parts = []
        
        for i, case in enumerate(similar_cases, 1):
            metadata = case['metadata']
            doc = case['document']
            
            context_parts.append(f"""
Example {i}:
{doc}

Source: {metadata.get('source', 'Unknown')}
Relevance Score: {1 - case.get('distance', 0):.2f}
""")
        
        return "\n".join(context_parts)
    
    def _create_consultation_prompt(
        self, 
        problem: str, 
        context: Optional[str],
        retrieved_cases: str
    ) -> str:
        """Create prompt for LLM consultation"""
        
        prompt = f"""You are an expert AI/ML consultant. A client has described a business problem, and you need to recommend appropriate AI/ML/DL/RL techniques and approaches.

CLIENT'S PROBLEM:
{problem}
"""
        
        if context:
            prompt += f"""
ADDITIONAL CONTEXT:
{context}
"""
        
        prompt += f"""
SIMILAR USE CASES FROM KNOWLEDGE BASE:
{retrieved_cases}

Based on the client's problem and similar use cases, provide a structured recommendation:

1. PROBLEM ANALYSIS
   - Restate the problem in technical terms
   - Identify the type of problem (classification, regression, generation, optimization, etc.)
   - Identify the data types involved

2. RECOMMENDED APPROACH
   - Should this use ML, DL, RL, or a combination?
   - Why is this approach appropriate?
   - What are the key requirements (data, compute, expertise)?

3. SPECIFIC TECHNIQUES & MODELS
   - List specific algorithms, architectures, or models
   - For each, explain why it's suitable
   - Mention any proven alternatives

4. IMPLEMENTATION CONSIDERATIONS
   - Data requirements (quantity, quality, labeling)
   - Potential challenges or limitations
   - ROI and feasibility factors

5. SIMILAR SUCCESS STORIES
   - Reference the most relevant example from the knowledge base
   - Explain how it relates to this problem

BE SPECIFIC AND PRACTICAL. Don't just say "use deep learning" - explain which architecture and why.
If the problem is NOT suitable for AI/ML, say so and explain why a traditional approach might be better.
"""
        
        return prompt
    
    def _query_llm(self, prompt: str) -> str:
        """Query the LLM with the constructed prompt"""
        
        if self.llm_provider == "groq":
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI/ML consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        elif self.llm_provider == "anthropic":
            response = self.llm_client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        
        elif self.llm_provider == "openai":
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI/ML consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            return response.choices[0].message.content
    
    def _calculate_confidence(self, similar_cases: List[Dict]) -> str:
        """Calculate confidence level based on similarity scores"""
        
        if not similar_cases:
            return "Low"
        
        avg_distance = sum(case.get('distance', 1.0) for case in similar_cases) / len(similar_cases)
        avg_similarity = 1 - avg_distance
        
        if avg_similarity > 0.8:
            return "High"
        elif avg_similarity > 0.6:
            return "Medium"
        else:
            return "Low"
    
    def interactive_mode(self):
        """Run in interactive mode for testing"""
        
        print("\n" + "="*60)
        print("🤖 AI Consultant Chatbot")
        print("="*60)
        print("Describe your business problem, and I'll suggest AI/ML/DL/RL solutions.")
        print("Type 'quit' or 'exit' to stop.\n")
        
        while True:
            problem = input("\n💼 Your problem: ").strip()
            
            if problem.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not problem:
                continue
            
            context = input("📝 Additional context (optional, press Enter to skip): ").strip()
            
            print("\n🔍 Analyzing problem and searching knowledge base...")
            
            result = self.suggest(
                problem=problem,
                context=context if context else None
            )
            
            print("\n" + "="*60)
            print("📊 RECOMMENDATION")
            print("="*60)
            print(result['recommendations'])
            print(f"\n🎯 Confidence: {result['confidence']}")
            print(f"📚 Based on {len(result['similar_cases'])} similar use cases")


def main():
    """Main entry point"""
    import argparse
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='AI Consultant Chatbot')
    parser.add_argument(
        '--mode',
        choices=['interactive', 'api'],
        default='interactive',
        help='Run mode'
    )
    parser.add_argument(
        '--problem',
        type=str,
        help='Problem description (for API mode)'
    )
    parser.add_argument(
        '--provider',
        choices=['groq', 'anthropic', 'openai'],
        default='groq',
        help='LLM provider'
    )
    
    args = parser.parse_args()
    
    # Check for API keys
    if args.provider == 'groq' and not os.getenv('GROQ_API_KEY'):
        print("⚠️  GROQ_API_KEY not found in environment")
        print("Please set it in your .env file")
        print("Get your free API key at: https://console.groq.com/")
        return
    
    if args.provider == 'anthropic' and not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  ANTHROPIC_API_KEY not found in environment")
        print("Please set it in your .env file")
        return
    
    if args.provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not found in environment")
        print("Please set it in your .env file")
        return
    
    # Initialize consultant
    consultant = AIConsultant(llm_provider=args.provider)
    
    if args.mode == 'interactive':
        consultant.interactive_mode()
    
    elif args.mode == 'api':
        if not args.problem:
            print("Error: --problem required for API mode")
            return
        
        result = consultant.suggest(problem=args.problem)
        
        print("\n" + "="*60)
        print("📊 RECOMMENDATION")
        print("="*60)
        print(result['recommendations'])
        print(f"\n🎯 Confidence: {result['confidence']}")


if __name__ == '__main__':
    main()
