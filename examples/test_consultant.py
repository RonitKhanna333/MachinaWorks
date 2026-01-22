"""
Test examples for AI Consultant
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from chatbot.consultant import AIConsultant
from dotenv import load_dotenv

load_dotenv()


def test_consultant():
    """Test the AI consultant with various problems"""
    
    print("\n" + "="*80)
    print("🧪 TESTING AI CONSULTANT")
    print("="*80 + "\n")
    
    # Initialize consultant
    print("Initializing consultant...")
    consultant = AIConsultant(llm_provider="groq")
    
    # Test cases
    test_problems = [
        {
            "problem": "We need to automate invoice processing from PDFs",
            "context": "Finance department, 10,000 invoices per month, mix of scanned and digital PDFs"
        },
        {
            "problem": "Customer churn prediction for subscription service",
            "context": "E-commerce SaaS, 50k users, have historical data on usage patterns and cancellations"
        },
        {
            "problem": "Real-time product recommendations on e-commerce website",
            "context": "Online retail, millions of products, need instant recommendations based on browsing"
        },
        {
            "problem": "Optimize warehouse robot navigation paths",
            "context": "Large warehouse with dynamic obstacles, robots need to learn optimal paths"
        },
        {
            "problem": "Detect fraudulent transactions in real-time",
            "context": "Payment processor, processing 1M+ transactions per day"
        }
    ]
    
    for i, test_case in enumerate(test_problems, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}")
        print(f"{'='*80}")
        print(f"Problem: {test_case['problem']}")
        print(f"Context: {test_case['context']}")
        print(f"\n{'Analyzing...':-^80}\n")
        
        result = consultant.suggest(
            problem=test_case['problem'],
            context=test_case['context']
        )
        
        print("📊 RECOMMENDATION:")
        print("-" * 80)
        print(result['recommendations'])
        print(f"\n🎯 Confidence: {result['confidence']}")
        print(f"📚 Based on {len(result['similar_cases'])} similar use cases")
        
        # Show top similar case
        if result['similar_cases']:
            top_case = result['similar_cases'][0]
            print(f"\n🔍 Most Similar Case:")
            print(f"   Source: {top_case['metadata'].get('source', 'Unknown')}")
            print(f"   Similarity: {(1 - top_case.get('distance', 1)) * 100:.1f}%")
        
        input("\nPress Enter to continue to next test case...\n")
    
    print("\n" + "="*80)
    print("✅ Testing complete!")
    print("="*80 + "\n")


if __name__ == '__main__':
    test_consultant()
