"""
Test script for Business Impact Analyzer

Demonstrates how to use the impact analyzer standalone.
"""

import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from chatbot.impact_analyzer import BusinessImpactAnalyzer


def test_impact_analysis():
    """Test the impact analyzer with sample scenarios"""
    
    print("\n" + "="*80)
    print("🧪 TESTING BUSINESS IMPACT ANALYZER")
    print("="*80)
    
    # Initialize analyzer
    analyzer = BusinessImpactAnalyzer(llm_provider="groq")
    
    # Test Case 1: Customer Service Automation
    print("\n\n📋 TEST CASE 1: Customer Service Automation")
    print("-" * 80)
    
    problem1 = """Our customer service team handles 10,000 support tickets monthly. 
    Average response time is 24 hours, resolution takes 3-5 days. 
    Customer satisfaction score is 3.2/5. Team of 20 agents costs $80K/month."""
    
    solution1 = """Implement AI chatbot with NLP for tier-1 support, 
    automated ticket classification, sentiment analysis, and RAG-based knowledge retrieval."""
    
    impact1 = analyzer.analyze(
        problem=problem1,
        ai_solution=solution1,
        industry="SaaS",
        company_size="SMB"
    )
    
    print(impact1.format_report())
    
    
    # Test Case 2: Predictive Maintenance
    print("\n\n📋 TEST CASE 2: Predictive Maintenance")
    print("-" * 80)
    
    problem2 = """Manufacturing plant has 500 machines. Unplanned downtime costs $50K/hour. 
    Currently using calendar-based maintenance. 200 hours of unplanned downtime annually."""
    
    solution2 = """Deploy IoT sensors with ML-based predictive maintenance models 
    using time-series analysis, anomaly detection, and failure prediction."""
    
    impact2 = analyzer.analyze(
        problem=problem2,
        ai_solution=solution2,
        industry="Manufacturing",
        company_size="enterprise"
    )
    
    print(impact2.format_report())
    
    
    # Test Case 3: Fraud Detection
    print("\n\n📋 TEST CASE 3: Fraud Detection")
    print("-" * 80)
    
    problem3 = """E-commerce platform processes 1M transactions monthly. 
    0.5% fraud rate results in $500K annual losses. Manual review catches only 60% of fraud."""
    
    solution3 = """Implement real-time fraud detection using ensemble ML models, 
    behavioral analysis, graph neural networks for relationship detection."""
    
    impact3 = analyzer.analyze(
        problem=problem3,
        ai_solution=solution3,
        industry="E-commerce",
        company_size="enterprise"
    )
    
    print(impact3.format_report())
    
    
    print("\n\n" + "="*80)
    print("✅ TESTING COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_impact_analysis()
