#!/usr/bin/env python
"""
Test Gemini API Integration
Verify that Gemini API key works and can generate content
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from news.ai_pipeline.orchestrator import AINewsOrchestrator


def test_gemini_direct():
    """Test direct Gemini API call"""
    print("=" * 60)
    print("TEST 1: Direct Gemini API Call")
    print("=" * 60)
    
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment")
            return False
        
        print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
        
        # Initialize Gemini
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            max_output_tokens=1000,
            google_api_key=api_key
        )
        print("✓ Gemini model initialized")
        
        # Test generation
        messages = [
            SystemMessage(content="You are a helpful AI assistant for a news website."),
            HumanMessage(content="Write a brief headline about AI technology advancements.")
        ]
        
        print("\n🤖 Generating content...")
        response = llm.invoke(messages)
        print(f"\n✅ Response received:")
        print(f"   {response.content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_orchestrator():
    """Test Orchestrator with Gemini"""
    print("\n" + "=" * 60)
    print("TEST 2: Orchestrator Initialization")
    print("=" * 60)
    
    try:
        orchestrator = AINewsOrchestrator()
        print("✓ Orchestrator initialized")
        print(f"   Primary LLM: {orchestrator.llm_primary.__class__.__name__}")
        print(f"   Config: {orchestrator.config.get('default_model')}")
        
        if orchestrator.llm_secondary:
            print(f"   Secondary LLM: {orchestrator.llm_secondary.__class__.__name__}")
        else:
            print("   Secondary LLM: None (optional)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_generation():
    """Test simple content generation through orchestrator"""
    print("\n" + "=" * 60)
    print("TEST 3: Simple Content Generation")
    print("=" * 60)
    
    try:
        orchestrator = AINewsOrchestrator()
        
        # Test keyword analysis stage
        test_keyword = "Artificial Intelligence breakthroughs in 2025"
        print(f"📝 Testing keyword: {test_keyword}")
        
        # Create a simple prompt
        messages = [
            SystemMessage(content="You are an AI news analyst. Provide concise, factual analysis."),
            HumanMessage(content=f"Analyze this news topic and suggest 3 article angles: {test_keyword}")
        ]
        
        print("\n🤖 Generating analysis...")
        response = orchestrator.llm_primary.invoke(messages)
        
        print(f"\n✅ Generated analysis:")
        print(f"{response.content[:400]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "🧪 " * 20)
    print("GEMINI API INTEGRATION TEST SUITE")
    print("🧪 " * 20 + "\n")
    
    results = {
        "Direct API Call": test_gemini_direct(),
        "Orchestrator Init": test_orchestrator(),
        "Content Generation": test_simple_generation()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Gemini integration is working!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
