#!/usr/bin/env python
"""
Phase 3 Testing Script
Tests Core Pipeline Tools

Run: python test_phase3.py
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
import django
django.setup()

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    print(f"\n{BLUE}{'=' * 70}\n{text}\n{'=' * 70}{RESET}\n")


def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    print(f"{RED}✗ {text}{RESET}")


def print_info(text):
    print(f"{YELLOW}ℹ {text}{RESET}")


def test_bias_detector():
    """Test BiasDetectionTool."""
    print_header("TEST 1: Bias Detector")
    
    try:
        from news.ai_pipeline.tools.bias_detector import BiasDetectionTool
        print_success("BiasDetectionTool imported")
        
        detector = BiasDetectionTool()
        
        # Test with biased content
        biased_text = """
        This shocking revelation about the corrupt politicians is absolutely devastating.
        The far-left radicals are destroying our country with their socialist agenda.
        Everyone knows this is a complete disaster and a total catastrophe.
        """
        
        result = detector.detect_bias(biased_text, "Political News")
        
        print_info(f"Bias Score: {result['bias_score']:.2f}% (target: <20%)")
        print_info(f"Passes Threshold: {result['passes_threshold']}")
        print_info(f"Political Lean: {result['rule_based_analysis']['political_lean']}")
        
        if result['bias_score'] > 30:  # Should detect high bias
            print_success("Correctly detected biased content")
        else:
            print_error("Failed to detect obvious bias")
        
        # Test with neutral content
        neutral_text = """
        According to the Bureau of Labor Statistics, unemployment fell to 3.5% in 2023.
        Economists have different views on the impact. Dr. Smith from Harvard suggests
        this indicates economic growth, while Professor Jones from MIT notes concerns
        about wage stagnation. The data shows mixed signals across sectors.
        """
        
        neutral_result = detector.detect_bias(neutral_text, "Economic News")
        print_info(f"Neutral Text Bias Score: {neutral_result['bias_score']:.2f}%")
        
        if neutral_result['bias_score'] < 20:
            print_success("Correctly identified neutral content")
            return True
        else:
            print_error("False positive on neutral content")
            return False
            
    except Exception as e:
        print_error(f"Bias detector test failed: {e}")
        return False


def test_fact_verifier():
    """Test FactVerificationTool."""
    print_header("TEST 2: Fact Verifier")
    
    try:
        from news.ai_pipeline.tools.fact_verifier import FactVerificationTool
        print_success("FactVerificationTool imported")
        
        verifier = FactVerificationTool()
        
        # Test with well-cited content
        cited_text = """
        Unemployment dropped to 3.5% in 2023, according to the Bureau of Labor Statistics.
        A study by Harvard University found that 67% of economists predict growth.
        "The data is encouraging," said Dr. Jane Smith, Chief Economist at the Federal Reserve.
        Research published in Nature showed a 15% increase in renewable energy adoption.
        """
        
        result = verifier.verify_facts(cited_text, "Economic Report")
        
        print_info(f"Total Claims: {result['total_claims']}")
        print_info(f"Cited Claims: {result['cited_claims']}")
        print_info(f"Verification Score: {result['verification_score']:.2f}% (target: >80%)")
        print_info(f"Passes Threshold: {result['passes_threshold']}")
        
        if result['verification_score'] >= 70:  # Should have good citation rate
            print_success("Correctly verified well-cited content")
        else:
            print_error(f"Unexpectedly low verification score")
        
        # Test source credibility
        if result['source_credibility']['sources']:
            print_info(f"Sources Found: {len(result['source_credibility']['sources'])}")
            print_info(f"Avg Credibility: {result['source_credibility']['average_credibility']:.1f}/100")
            print_success("Source credibility analysis working")
            return True
        else:
            print_error("Failed to extract sources")
            return False
            
    except Exception as e:
        print_error(f"Fact verifier test failed: {e}")
        return False


def test_perspective_analyzer():
    """Test PerspectiveAnalyzer."""
    print_header("TEST 3: Perspective Analyzer")
    
    try:
        from news.ai_pipeline.tools.perspective_analyzer import PerspectiveAnalyzer
        print_success("PerspectiveAnalyzer imported")
        
        analyzer = PerspectiveAnalyzer()
        
        # Test with multi-perspective content
        multi_perspective_text = """
        The new climate policy has sparked debate. Supporters argue it will reduce
        emissions by 30%, according to the Environmental Protection Agency.
        
        However, critics say the economic costs are too high. "This will hurt 
        businesses," stated John Doe, CEO of Industry Coalition.
        
        On the other hand, environmental groups praise the initiative. "It's a 
        necessary step," according to Green Earth Foundation.
        
        Some economists suggest a middle ground approach, while others believe
        more aggressive action is needed.
        """
        
        result = analyzer.analyze_perspectives(multi_perspective_text, "Climate Policy")
        
        print_info(f"Perspectives Found: {result['perspective_count']} (target: ≥2)")
        print_info(f"Balance Score: {result['balance_score']:.2f}/100")
        print_info(f"Passes Threshold: {result['passes_threshold']}")
        
        if result['perspective_count'] >= 2:
            print_success("Correctly identified multiple perspectives")
        else:
            print_error("Failed to detect multiple perspectives")
        
        # Test with one-sided content
        one_sided_text = """
        The new policy is excellent and will benefit everyone. It's clearly the
        right approach and will solve all our problems. Everyone agrees this
        is the best solution.
        """
        
        one_sided_result = analyzer.analyze_perspectives(one_sided_text, "Policy")
        print_info(f"One-sided Content Perspectives: {one_sided_result['perspective_count']}")
        
        if one_sided_result['perspective_count'] < 2:
            print_success("Correctly flagged one-sided content")
            return True
        else:
            print_error("False positive on one-sided content")
            return False
            
    except Exception as e:
        print_error(f"Perspective analyzer test failed: {e}")
        return False


def test_integration():
    """Test tools working together."""
    print_header("TEST 4: Integration Test")
    
    try:
        from news.ai_pipeline.tools.bias_detector import BiasDetectionTool
        from news.ai_pipeline.tools.fact_verifier import FactVerificationTool
        from news.ai_pipeline.tools.perspective_analyzer import PerspectiveAnalyzer
        
        # Sample article
        article = """
        AI in Healthcare: A Balanced Look
        
        Artificial intelligence is transforming healthcare diagnostics, according to
        a 2024 study by Johns Hopkins University. The research found that AI systems
        achieved 94% accuracy in detecting certain cancers from medical imaging.
        
        Dr. Sarah Johnson, Chief of Radiology at Mayo Clinic, stated: "AI is a 
        powerful tool that enhances our diagnostic capabilities."
        
        However, some physicians express concerns. "We must ensure AI doesn't replace
        human judgment," warned Dr. Michael Chen from Stanford Medical Center.
        
        Critics also point to data privacy issues. The Electronic Frontier Foundation
        notes that medical AI systems require access to sensitive patient information.
        
        Proponents argue the benefits outweigh risks. According to a report by the
        World Health Organization, AI could save an estimated 250,000 lives annually
        by 2030 through earlier disease detection.
        """
        
        bias_detector = BiasDetectionTool()
        fact_verifier = FactVerificationTool()
        perspective_analyzer = PerspectiveAnalyzer()
        
        bias_result = bias_detector.detect_bias(article, "AI in Healthcare")
        fact_result = fact_verifier.verify_facts(article, "AI in Healthcare")
        perspective_result = perspective_analyzer.analyze_perspectives(article, "AI in Healthcare")
        
        print_info("Quality Scores:")
        print(f"  Bias: {bias_result['bias_score']:.1f}% (target: <20%) - {'✓' if bias_result['passes_threshold'] else '✗'}")
        print(f"  Facts: {fact_result['verification_score']:.1f}% (target: >80%) - {'✓' if fact_result['passes_threshold'] else '✗'}")
        print(f"  Perspectives: {perspective_result['perspective_count']} (target: ≥2) - {'✓' if perspective_result['passes_threshold'] else '✗'}")
        
        all_pass = (
            bias_result['passes_threshold'] and
            fact_result['passes_threshold'] and
            perspective_result['passes_threshold']
        )
        
        if all_pass:
            print_success("All quality checks passed!")
            print_info("This article meets AI Analitica standards")
            return True
        else:
            print_error("Some quality checks failed")
            if not bias_result['passes_threshold']:
                print_info(f"  Bias too high: {bias_result['bias_score']:.1f}%")
            if not fact_result['passes_threshold']:
                print_info(f"  Citations insufficient: {fact_result['verification_score']:.1f}%")
            if not perspective_result['passes_threshold']:
                print_info(f"  Not enough perspectives: {perspective_result['perspective_count']}")
            return False
            
    except Exception as e:
        print_error(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_performance():
    """Test tool performance with various inputs."""
    print_header("TEST 5: Performance & Edge Cases")
    
    try:
        from news.ai_pipeline.tools.bias_detector import BiasDetectionTool
        
        detector = BiasDetectionTool()
        
        # Test empty string
        try:
            result = detector.detect_bias("", "")
            print_success("Handles empty input")
        except Exception as e:
            print_error(f"Failed on empty input: {e}")
            return False
        
        # Test very short content
        result = detector.detect_bias("This is news.", "Short")
        print_success("Handles short content")
        
        # Test long content
        long_text = " ".join(["This is a sentence about politics and economics."] * 100)
        result = detector.detect_bias(long_text, "Long Article")
        print_success("Handles long content")
        print_info(f"Long article bias score: {result['bias_score']:.1f}%")
        
        return True
        
    except Exception as e:
        print_error(f"Performance test failed: {e}")
        return False


def main():
    """Run all Phase 3 tests."""
    print_header("🔧 PHASE 3 CORE TOOLS TESTS")
    
    results = {
        'Bias Detector': test_bias_detector(),
        'Fact Verifier': test_fact_verifier(),
        'Perspective Analyzer': test_perspective_analyzer(),
        'Integration': test_integration(),
        'Performance': test_tool_performance(),
    }
    
    # Summary
    print_header("📊 TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{test_name:.<50} {status}")
    
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    
    if passed == total:
        print(f"{GREEN}✅ Phase 3 Implementation: SUCCESSFUL{RESET}")
        print(f"{GREEN}All {total} test categories passed!{RESET}")
        print(f"\n{YELLOW}Tools Implemented:{RESET}")
        print("• BiasDetectionTool (397 lines) - <20% bias standard")
        print("• FactVerificationTool (422 lines) - >80% citation requirement")
        print("• PerspectiveAnalyzer (205 lines) - ≥2 viewpoints required")
        print(f"\n{YELLOW}Next Steps:{RESET}")
        print("1. Implement remaining tools (optional):")
        print("   - ResearchAgent (web search, NewsAPI)")
        print("   - ContentGenerationChain")
        print("   - AIDetector, PlagiarismChecker")
        print("\n2. Or proceed to Phase 4: Celery async processing")
        print("\n3. Test with real API keys for LLM-enhanced analysis")
    else:
        print(f"{YELLOW}⚠️  Phase 3 Implementation: PARTIAL{RESET}")
        print(f"{passed}/{total} test categories passed")
    
    print(f"{BLUE}{'=' * 70}{RESET}\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
