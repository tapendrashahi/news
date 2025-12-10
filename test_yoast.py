#!/usr/bin/env python
"""
Test YoastSEO integration
"""

import os
import sys
import django

# Add project to path
sys.path.insert(0, '/home/tapendra/Downloads/projects/news')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')
django.setup()

from news.ai_pipeline.yoast_seo import get_yoast_service

def test_yoast():
    print("=" * 60)
    print("Testing YoastSEO Integration")
    print("=" * 60)
    
    # Get service instance
    yoast = get_yoast_service()
    
    # Test 1: Health check
    print("\n1. Health Check:")
    health = yoast.health_check()
    print(f"   Status: {health['status']}")
    print(f"   Message: {health['message']}")
    print(f"   Using Fallback: {health['using_fallback']}")
    
    if health['status'] == 'error':
        print("\n❌ YoastSEO is not available. Will use fallback mode.")
        # Continue with tests to show fallback works
    
    # Test 2: Basic SEO analysis
    print("\n2. Basic SEO Analysis:")
    test_content = """
    <h1>Understanding Artificial Intelligence</h1>
    <p>Artificial intelligence (AI) is revolutionizing technology and business. 
    AI systems can learn from data and make intelligent decisions.</p>
    <p>Machine learning, a subset of artificial intelligence, enables computers 
    to learn without being explicitly programmed. Deep learning takes this further 
    with neural networks.</p>
    <p>The applications of artificial intelligence span across healthcare, finance, 
    transportation, and entertainment. AI is transforming how we work and live.</p>
    """
    
    analysis = yoast.analyze_content(
        content=test_content,
        title="Understanding Artificial Intelligence: A Comprehensive Guide",
        focus_keyword="artificial intelligence",
        meta_description="Discover how artificial intelligence is transforming technology, business, and daily life with machine learning and deep learning."
    )
    
    print(f"   SEO Score: {analysis['seo_score']}/100")
    print(f"   SEO Rating: {analysis['seo_rating']}")
    print(f"   Readability Score: {analysis['readability_score']}/100")
    print(f"   Keyword Density: {analysis['keyword_density']:.2f}%")
    print(f"   Keyword in Title: {'✅' if analysis['keyword_in_title'] else '❌'}")
    print(f"   Keyword in Description: {'✅' if analysis['keyword_in_description'] else '❌'}")
    
    if analysis.get('issues'):
        print(f"\n   ⚠️  Issues ({len(analysis['issues'])}):")
        for issue in analysis['issues']:
            print(f"      - {issue}")
    
    if analysis.get('improvements'):
        print(f"\n   💡 Improvements ({len(analysis['improvements'])}):")
        for improvement in analysis['improvements']:
            print(f"      - {improvement}")
    
    if analysis.get('good_results'):
        print(f"\n   ✅ Good Results ({len(analysis['good_results'])}):")
        for result in analysis['good_results']:
            print(f"      - {result}")
    
    # Test 3: Poor content
    print("\n3. Testing Poor Content:")
    poor_content = "<p>This is a short article.</p>"
    
    poor_analysis = yoast.analyze_content(
        content=poor_content,
        title="Article",
        focus_keyword="test",
        meta_description=""
    )
    
    print(f"   SEO Score: {poor_analysis['seo_score']}/100")
    print(f"   Issues: {len(poor_analysis.get('issues', []))}")
    
    # Test 4: Recommendations
    print("\n4. Getting Optimization Suggestions:")
    suggestions = yoast.optimize_content(test_content, 
                                         "Understanding Artificial Intelligence: A Comprehensive Guide",
                                         "artificial intelligence",
                                         analysis)
    
    if suggestions.get('overall_priority'):
        print(f"   Priority Issues: {len(suggestions['overall_priority'])}")
        for i, issue in enumerate(suggestions['overall_priority'][:3], 1):
            print(f"   {i}. {issue}")
    
    if suggestions.get('content_suggestions'):
        print(f"\n   Content Improvements:")
        for i, sug in enumerate(suggestions['content_suggestions'][:3], 1):
            print(f"   {i}. {sug}")
    
    print("\n" + "=" * 60)
    print("✅ YoastSEO Integration Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_yoast()
