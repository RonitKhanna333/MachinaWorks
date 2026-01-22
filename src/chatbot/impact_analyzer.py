"""
Business Impact Analyzer

Analyzes and quantifies the business impact of AI solutions.
Provides ROI estimates, cost savings, revenue opportunities, and implementation insights.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Try different LLM providers
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BusinessImpact:
    """Structured business impact analysis"""
    cost_savings: str
    revenue_potential: str
    time_savings: str
    roi_estimate: str
    risk_reduction: str
    competitive_advantage: str
    implementation_timeline: str
    resource_requirements: str
    key_metrics: List[str]
    success_factors: List[str]
    potential_challenges: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "cost_savings": self.cost_savings,
            "revenue_potential": self.revenue_potential,
            "time_savings": self.time_savings,
            "roi_estimate": self.roi_estimate,
            "risk_reduction": self.risk_reduction,
            "competitive_advantage": self.competitive_advantage,
            "implementation_timeline": self.implementation_timeline,
            "resource_requirements": self.resource_requirements,
            "key_metrics": self.key_metrics,
            "success_factors": self.success_factors,
            "potential_challenges": self.potential_challenges
        }
    
    def format_report(self) -> str:
        """Format as readable report"""
        report = "\n" + "="*80 + "\n"
        report += "📊 BUSINESS IMPACT ANALYSIS\n"
        report += "="*80 + "\n\n"
        
        report += "💰 COST SAVINGS\n"
        report += f"{self.cost_savings}\n\n"
        
        report += "📈 REVENUE POTENTIAL\n"
        report += f"{self.revenue_potential}\n\n"
        
        report += "⏱️ TIME SAVINGS\n"
        report += f"{self.time_savings}\n\n"
        
        report += "💵 ROI ESTIMATE\n"
        report += f"{self.roi_estimate}\n\n"
        
        report += "🛡️ RISK REDUCTION\n"
        report += f"{self.risk_reduction}\n\n"
        
        report += "🚀 COMPETITIVE ADVANTAGE\n"
        report += f"{self.competitive_advantage}\n\n"
        
        report += "📅 IMPLEMENTATION TIMELINE\n"
        report += f"{self.implementation_timeline}\n\n"
        
        report += "👥 RESOURCE REQUIREMENTS\n"
        report += f"{self.resource_requirements}\n\n"
        
        report += "📊 KEY METRICS TO TRACK\n"
        for metric in self.key_metrics:
            report += f"  • {metric}\n"
        report += "\n"
        
        report += "✅ SUCCESS FACTORS\n"
        for factor in self.success_factors:
            report += f"  • {factor}\n"
        report += "\n"
        
        report += "⚠️ POTENTIAL CHALLENGES\n"
        for challenge in self.potential_challenges:
            report += f"  • {challenge}\n"
        
        report += "\n" + "="*80 + "\n"
        
        return report


class BusinessImpactAnalyzer:
    """
    Analyzes business impact of AI solutions using LLMs.
    
    Features:
    - Cost-benefit analysis
    - ROI estimation
    - Time and resource planning
    - Risk assessment
    - Success metrics definition
    """
    
    def __init__(
        self,
        llm_provider: str = "groq",
        model: Optional[str] = None
    ):
        """
        Initialize the business impact analyzer.
        
        Args:
            llm_provider: LLM provider to use ("groq", "anthropic", or "openai")
            model: Specific model to use (optional, uses defaults)
        """
        self.llm_provider = llm_provider.lower()
        self.model = model
        
        # Initialize LLM client
        if self.llm_provider == "groq" and GROQ_AVAILABLE:
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model = model or "llama-3.3-70b-versatile"
        elif self.llm_provider == "anthropic" and ANTHROPIC_AVAILABLE:
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = model or "claude-3-5-sonnet-20241022"
        elif self.llm_provider == "openai" and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = model or "gpt-4-turbo-preview"
        else:
            raise ValueError(f"LLM provider '{llm_provider}' not available or not supported")
        
        logger.info(f"✅ Initialized BusinessImpactAnalyzer with {self.llm_provider} ({self.model})")
    
    def analyze(
        self,
        problem: str,
        ai_solution: str,
        industry: Optional[str] = None,
        company_size: Optional[str] = None
    ) -> BusinessImpact:
        """
        Analyze business impact of an AI solution.
        
        Args:
            problem: The business problem
            ai_solution: The proposed AI solution
            industry: Industry context (optional)
            company_size: Company size (optional, e.g., "startup", "SMB", "enterprise")
        
        Returns:
            BusinessImpact object with detailed analysis
        """
        logger.info("Analyzing business impact...")
        
        # Build context
        context = f"Business Problem: {problem}\n\n"
        context += f"Proposed AI Solution: {ai_solution}\n\n"
        if industry:
            context += f"Industry: {industry}\n\n"
        if company_size:
            context += f"Company Size: {company_size}\n\n"
        
        # Create analysis prompt
        prompt = self._create_analysis_prompt(context)
        
        # Query LLM
        response = self._query_llm(prompt)
        
        # Debug output
        logger.info(f"\\n\\nLLM RESPONSE:\\n{response}\\n\\n")
        
        # Parse response
        impact = self._parse_impact_response(response)
        
        return impact
    
    def _create_analysis_prompt(self, context: str) -> str:
        """Create detailed analysis prompt"""
        prompt = f"""You are a business impact analyst specializing in AI/ML implementations.

{context}

Provide a comprehensive business impact analysis covering:

1. COST SAVINGS: Quantify potential cost reductions (labor, operations, errors, etc.). Use specific percentages and examples.

2. REVENUE POTENTIAL: Identify new revenue opportunities or growth potential. Be specific about mechanisms.

3. TIME SAVINGS: Estimate time saved in processes, decision-making, or operations. Use concrete numbers.

4. ROI ESTIMATE: Provide realistic ROI timeline and percentage. Consider implementation costs.

5. RISK REDUCTION: Explain how AI reduces business risks (compliance, errors, fraud, etc.).

6. COMPETITIVE ADVANTAGE: Describe strategic advantages gained through AI adoption.

7. IMPLEMENTATION TIMELINE: Realistic timeline from planning to full deployment (weeks/months).

8. RESOURCE REQUIREMENTS: Team size, skills needed, infrastructure, budget estimates.

9. KEY METRICS: List 5-7 specific KPIs to track success.

10. SUCCESS FACTORS: List 4-6 critical factors for successful implementation.

11. POTENTIAL CHALLENGES: List 4-6 realistic challenges and risks to consider.

Format your response as structured sections with clear headings. Be specific, quantitative where possible, and realistic."""

        return prompt
    
    def _query_llm(self, prompt: str) -> str:
        """Query the LLM"""
        try:
            if self.llm_provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a business impact analyst with expertise in AI/ML ROI and implementation."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=3000,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                return response.content[0].text
            
            elif self.llm_provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a business impact analyst with expertise in AI/ML ROI and implementation."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error querying LLM: {str(e)}")
            raise
    
    def _parse_impact_response(self, response: str) -> BusinessImpact:
        """Parse LLM response into structured BusinessImpact"""
        
        # Debug: log the response
        logger.debug(f"Parsing response (first 500 chars): {response[:500]}")
        
        # Helper function to extract section content
        def extract_section(text: str, section_name: str) -> str:
            # Try multiple patterns with case-insensitive matching
            import re
            
            patterns = [
                rf"###\s*\d+\.\s*{re.escape(section_name)}[:\s]*\n(.*?)(?=\n###|\n##|\Z)",  # ### 1. SECTION
                rf"##\s*{re.escape(section_name)}[:\s]*\n(.*?)(?=\n###|\n##|\Z)",  # ## SECTION
                rf"###\s*{re.escape(section_name)}[:\s]*\n(.*?)(?=\n###|\n##|\Z)",  # ### SECTION
                rf"\*\*{re.escape(section_name)}\*\*[:\s]*\n(.*?)(?=\n\*\*|\n##|\n###|\Z)",  # **SECTION**
                rf"{re.escape(section_name)}[:\s]*\n(.*?)(?=\n\n[A-Z]|\n##|\n###|\Z)",  # SECTION:\n
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    if content:
                        # Remove bullet points at the start if present
                        content = re.sub(r'^[-*•]\s*', '', content)
                        return content
            
            return "Analysis not available"
        
        # Helper to extract list items
        def extract_list_items(text: str, section_name: str) -> List[str]:
            import re
            
            section_text = extract_section(text, section_name)
            if section_text == "Analysis not available":
                return ["To be determined during detailed analysis"]
            
            # Pre-processing: Handle inline lists by inserting newlines before bullets
            # e.g. "Intro: * Item 1 * Item 2" -> "Intro:\n* Item 1\n* Item 2"
            # Matches space followed by bullet followed by space
            section_text = re.sub(r'(\s+)([-•*]|\u26a0|\u26a1|\u2705|⚠|⚠️)(\s+)', r'\n\2\3', section_text)
            
            items = []
            
            # Split by newlines
            lines = section_text.split('\n')
            current_item = ""
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this is a new list item
                # Matches generic bullets, numbers, and common emojis
                is_new_item = re.match(r'^([-•*\d]+[.)]|\u26a0|\u26a1|\u2705|⚠|⚠️)\s+', line)
                
                if is_new_item:
                    # Save previous item if valid
                    if current_item:
                        items.append(current_item.strip())
                    
                    # Start new item
                    # Remove the bullet/number/emoji
                    cleaned = re.sub(r'^([-•*\d]+[.)]|\u26a0|\u26a1|\u2705|⚠|⚠️)\s+', '', line)
                    # Remove ** markers
                    cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
                    current_item = cleaned
                else:
                    # Continuation of previous item OR content following a standalone bullet
                    # Filter out purely intro sentences if we haven't started items yet
                    is_intro = line.strip().endswith(':') or "metrics are" in line.lower() or "factors are" in line.lower()
                    
                    if not current_item and is_intro:
                        continue
                        
                    if current_item:
                        current_item += " " + line
                    else:
                        # Case: No bullet yet, but not an intro. Treat as item if substantial.
                        # Exclude isolated emojis or symbols
                        if len(line) > 3 and not re.match(r'^[⚠⚠️:.]+$', line):
                            current_item = line
            
            # Don't forget the last item
            if current_item:
                items.append(current_item.strip())
            
            # Filter out empty items or items that are just short symbols/garbage
            items = [i for i in items if len(i) > 3 and not re.match(r'^[⚠⚠️:.]+$', i)]
            
            # Fallback to sentence splitting if we didn't find structured items
            if not items:
                sentences = [s.strip() for s in re.split(r'[.;]', section_text) if len(s.strip()) > 20]
                items = sentences[:5] if sentences else ["To be determined during detailed analysis"]
            
            return items
        
        # Extract all sections
        impact = BusinessImpact(
            cost_savings=extract_section(response, "COST SAVINGS"),
            revenue_potential=extract_section(response, "REVENUE POTENTIAL"),
            time_savings=extract_section(response, "TIME SAVINGS"),
            roi_estimate=extract_section(response, "ROI ESTIMATE"),
            risk_reduction=extract_section(response, "RISK REDUCTION"),
            competitive_advantage=extract_section(response, "COMPETITIVE ADVANTAGE"),
            implementation_timeline=extract_section(response, "IMPLEMENTATION TIMELINE"),
            resource_requirements=extract_section(response, "RESOURCE REQUIREMENTS"),
            key_metrics=extract_list_items(response, "KEY METRICS"),
            success_factors=extract_list_items(response, "SUCCESS FACTORS"),
            potential_challenges=extract_list_items(response, "POTENTIAL CHALLENGES")
        )
        
        return impact


def main():
    """Demo the business impact analyzer"""
    import sys
    
    # Example usage
    analyzer = BusinessImpactAnalyzer(llm_provider="groq")
    
    # Analyze a sample problem
    problem = "Our customer service team receives 10,000 support tickets per month. Response times average 24 hours and resolution takes 3-5 days. Customer satisfaction is declining."
    
    solution = "Implement an AI-powered customer service chatbot with natural language understanding, integrated with a RAG system containing all product documentation and support history. Include automated ticket classification and routing."
    
    print("\n" + "="*80)
    print("🤖 AI CONSULTANT - BUSINESS IMPACT ANALYSIS")
    print("="*80)
    print(f"\n📋 Problem: {problem}")
    print(f"\n💡 Solution: {solution}")
    print("\n⏳ Analyzing business impact...\n")
    
    impact = analyzer.analyze(
        problem=problem,
        ai_solution=solution,
        industry="SaaS",
        company_size="SMB"
    )
    
    # Print formatted report
    print(impact.format_report())
    
    # Also available as dict
    # impact_dict = impact.to_dict()
    # print(json.dumps(impact_dict, indent=2))


if __name__ == "__main__":
    main()
