"""
Test script to verify the backend API is working correctly
"""

import requests
import json

def test_health():
    """Test if the server is running"""
    print("\n" + "="*60)
    print("Testing Backend Health...")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✓ Server is running")
        print(f"  Status: {response.status_code}")
        data = response.json()
        print(f"  Components:")
        for key, value in data.get("components", {}).items():
            status = "✓" if value else "✗"
            print(f"    {status} {key}: {value}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running!")
        print("  Start it with: python src/api/server.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_consultation():
    """Test the consultation endpoint"""
    print("\n" + "="*60)
    print("Testing AI Consultation...")
    print("="*60)
    
    test_request = {
        "problem": "Our customer service team costs $50K/month handling 5,000 support tickets. Average response time is 12 hours, and CSAT score is 3.5/5. We need to reduce costs while improving service quality.",
        "industry": "SaaS",
        "companySize": "SMB",
        "email": "test@example.com"
    }
    
    print(f"\nRequest:")
    print(f"  Industry: {test_request['industry']}")
    print(f"  Company Size: {test_request['companySize']}")
    print(f"  Problem: {test_request['problem'][:80]}...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/consult",
            json=test_request,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✓ Success!")
            print(f"\nRecommendations Preview:")
            recommendations = data.get("recommendations", "")
            print(f"  {recommendations[:200]}...")
            print(f"  Length: {len(recommendations)} characters")
            
            if data.get("businessImpact"):
                print(f"\n✓ Business Impact Analysis:")
                impact = data["businessImpact"]
                print(f"  Cost Savings: {impact.get('cost_savings', 'N/A')[:60]}...")
                print(f"  ROI Estimate: {impact.get('roi_estimate', 'N/A')[:60]}...")
                print(f"  Timeline: {impact.get('implementation_timeline', 'N/A')[:60]}...")
            else:
                print(f"\n✗ No business impact data returned")
            
            # Check if it's mock or real
            if "Mock response" in recommendations or "demonstration" in recommendations.lower():
                print(f"\n⚠ WARNING: Received mock data!")
                print(f"  This means the AI backend is not fully functional.")
                print(f"  Possible issues:")
                print(f"    1. Vector store is empty - run: python quick_start.py")
                print(f"    2. GROQ_API_KEY not set in .env")
                print(f"    3. AI components failed to initialize")
            else:
                print(f"\n✅ Received real AI response!")
                
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"  {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"✗ Request timed out (>60s)")
        print(f"  The AI might be processing but taking too long")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    print("\n" + "="*60)
    print("  AI Consultancy Backend Test Suite")
    print("="*60)
    
    # Test 1: Health check
    if not test_health():
        print("\n⚠ Cannot continue tests - server not running")
        return
    
    # Test 2: Consultation
    test_consultation()
    
    print("\n" + "="*60)
    print("Tests Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
