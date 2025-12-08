#!/usr/bin/env python
"""
Phase 2 Testing Script
Tests LangChain pipeline integration and prompt templates

Run: python test_phase2.py
"""

import os
import sys
import asyncio
from datetime import datetime

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
import django
django.setup()

# Now import Django models
from news.ai_models import AIArticle, AIGenerationConfig, KeywordSource
from news.ai_pipeline.prompts.article_templates import (
    SYSTEM_PROMPT,
    RESEARCH_PROMPT,
    OUTLINE_PROMPT,
    ARTICLE_GENERATION_PROMPT,
    get_template_guidance
)
from news.ai_pipeline.prompts.meta_prompts import (
    META_TITLE_PROMPT,
    META_DESCRIPTION_PROMPT,
    KEYWORDS_EXTRACTION_PROMPT,
    calculate_seo_score
)
from news.ai_pipeline.prompts.seo_prompts import (
    SEO_ANALYSIS_PROMPT,
    SEO_IMPROVEMENT_PROMPT,
    KEYWORD_DENSITY_PROMPT
)

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print section header."""
    print(f"\n{BLUE}{'=' * 70}")
    print(f"{text}")
    print(f"{'=' * 70}{RESET}\n")


def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")


def print_info(text):
    """Print info message."""
    print(f"{YELLOW}ℹ {text}{RESET}")


def test_imports():
    """Test that all Phase 2 dependencies are installed."""
    print_header("TEST 1: Import Dependencies")
    
    dependencies = [
        ('langchain', 'LangChain core'),
        ('langchain_openai', 'LangChain OpenAI'),
        ('langchain_anthropic', 'LangChain Anthropic'),
        ('openai', 'OpenAI SDK'),
        ('anthropic', 'Anthropic SDK'),
        ('tiktoken', 'Tiktoken tokenizer'),
    ]
    
    all_imported = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print_success(f"{display_name} imported successfully")
        except ImportError as e:
            print_error(f"Failed to import {display_name}: {e}")
            all_imported = False
    
    return all_imported


def test_prompt_templates():
    """Test that all prompt templates are loaded correctly."""
    print_header("TEST 2: Prompt Templates")
    
    tests_passed = 0
    total_tests = 0
    
    # Test SYSTEM_PROMPT
    total_tests += 1
    if "AI Analitica" in SYSTEM_PROMPT and "Bias Score" in SYSTEM_PROMPT:
        print_success("SYSTEM_PROMPT contains mission-aligned content")
        tests_passed += 1
    else:
        print_error("SYSTEM_PROMPT missing AI Analitica mission content")
    
    # Test RESEARCH_PROMPT
    total_tests += 1
    try:
        messages = RESEARCH_PROMPT.format_messages(
            keyword="AI in Healthcare",
            audience="General public",
            depth="Comprehensive",
            focus_angle="Medical applications"
        )
        if len(messages) == 2:  # system + human
            print_success("RESEARCH_PROMPT formatted successfully")
            tests_passed += 1
        else:
            print_error(f"RESEARCH_PROMPT has wrong message count: {len(messages)}")
    except Exception as e:
        print_error(f"RESEARCH_PROMPT formatting failed: {e}")
    
    # Test OUTLINE_PROMPT
    total_tests += 1
    try:
        messages = OUTLINE_PROMPT.format_messages(
            keyword="AI in Healthcare",
            template_type="analysis",
            word_count=1500,
            research_summary="Test summary"
        )
        if len(messages) == 2:
            print_success("OUTLINE_PROMPT formatted successfully")
            tests_passed += 1
        else:
            print_error(f"OUTLINE_PROMPT has wrong message count")
    except Exception as e:
        print_error(f"OUTLINE_PROMPT formatting failed: {e}")
    
    # Test ARTICLE_GENERATION_PROMPT
    total_tests += 1
    try:
        messages = ARTICLE_GENERATION_PROMPT.format_messages(
            outline="Test outline",
            research_data="Test research",
            template_type="analysis",
            tone="professional",
            word_count=1500
        )
        if len(messages) == 2:
            print_success("ARTICLE_GENERATION_PROMPT formatted successfully")
            tests_passed += 1
        else:
            print_error(f"ARTICLE_GENERATION_PROMPT has wrong message count")
    except Exception as e:
        print_error(f"ARTICLE_GENERATION_PROMPT formatting failed: {e}")
    
    # Test template guidance function
    total_tests += 1
    guidance = get_template_guidance('analysis')
    if "expert perspectives" in guidance.lower():
        print_success("Template guidance function works correctly")
        tests_passed += 1
    else:
        print_error("Template guidance function returned unexpected content")
    
    # Test META prompts
    total_tests += 1
    try:
        messages = META_TITLE_PROMPT.format_messages(
            headline="AI Transforms Healthcare Diagnosis",
            keyword="AI healthcare",
            summary="Article about AI in medical diagnosis"
        )
        if len(messages) == 2:
            print_success("META_TITLE_PROMPT formatted successfully")
            tests_passed += 1
        else:
            print_error(f"META_TITLE_PROMPT has wrong message count")
    except Exception as e:
        print_error(f"META_TITLE_PROMPT formatting failed: {e}")
    
    # Test SEO score calculator
    total_tests += 1
    score = calculate_seo_score(
        title_len=55,
        desc_len=155,
        keyword_density=1.5,
        has_headings=True,
        readability_score=65
    )
    if 90 <= score <= 100:
        print_success(f"SEO score calculator works correctly (score: {score})")
        tests_passed += 1
    else:
        print_error(f"SEO score calculator returned unexpected score: {score}")
    
    # Test SEO ANALYSIS PROMPT
    total_tests += 1
    try:
        messages = SEO_ANALYSIS_PROMPT.format_messages(
            title="Test Title",
            meta_description="Test description",
            slug="test-slug",
            word_count=1500,
            primary_keyword="test keyword",
            category="Technology",
            content="Test content"
        )
        if len(messages) == 2:
            print_success("SEO_ANALYSIS_PROMPT formatted successfully")
            tests_passed += 1
        else:
            print_error(f"SEO_ANALYSIS_PROMPT has wrong message count")
    except Exception as e:
        print_error(f"SEO_ANALYSIS_PROMPT formatting failed: {e}")
    
    print_info(f"\nPrompt Templates: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_orchestrator():
    """Test orchestrator class initialization."""
    print_header("TEST 3: AI News Orchestrator")
    
    try:
        from news.ai_pipeline.orchestrator import AINewsOrchestrator
        print_success("AINewsOrchestrator imported successfully")
        
        # Check if API keys are configured
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not openai_key:
            print_error("OPENAI_API_KEY not set in environment")
            print_info("Set API key: export OPENAI_API_KEY='your-key-here'")
        else:
            print_success("OPENAI_API_KEY found in environment")
        
        if not anthropic_key:
            print_error("ANTHROPIC_API_KEY not set in environment")
            print_info("Set API key: export ANTHROPIC_API_KEY='your-key-here'")
        else:
            print_success("ANTHROPIC_API_KEY found in environment")
        
        # Try to initialize (may fail without API keys, which is expected)
        try:
            config = {
                'openai_api_key': openai_key or 'test-key',
                'anthropic_api_key': anthropic_key or 'test-key',
                'default_model': 'gpt-4-turbo-preview',
                'temperature': 0.7,
            }
            # Don't actually initialize LLMs in test if no API keys
            if not openai_key:
                print_info("Skipping LLM initialization (no API keys)")
                return False
            
            orchestrator = AINewsOrchestrator(config=config)
            print_success("AINewsOrchestrator initialized successfully")
            
            # Check stage registration
            expected_stages = [
                'keyword_analysis', 'research', 'outline', 
                'content_generation', 'humanization', 'ai_detection',
                'plagiarism_check', 'bias_detection', 'fact_verification',
                'perspective_analysis', 'seo_optimization', 'meta_generation',
                'image_generation', 'finalization'
            ]
            
            missing_stages = [s for s in expected_stages if s not in orchestrator.stages]
            if not missing_stages:
                print_success(f"All {len(expected_stages)} pipeline stages registered")
            else:
                print_error(f"Missing stages: {', '.join(missing_stages)}")
            
            return len(missing_stages) == 0
            
        except Exception as e:
            print_error(f"Orchestrator initialization failed: {e}")
            if "API key" in str(e):
                print_info("This is expected if API keys are not configured")
            return False
            
    except ImportError as e:
        print_error(f"Failed to import orchestrator: {e}")
        return False


def test_models():
    """Test that AI models are accessible."""
    print_header("TEST 4: Django Models")
    
    tests_passed = 0
    
    # Test KeywordSource model
    try:
        count = KeywordSource.objects.count()
        print_success(f"KeywordSource model accessible ({count} records)")
        tests_passed += 1
    except Exception as e:
        print_error(f"KeywordSource model error: {e}")
    
    # Test AIArticle model
    try:
        count = AIArticle.objects.count()
        print_success(f"AIArticle model accessible ({count} records)")
        tests_passed += 1
    except Exception as e:
        print_error(f"AIArticle model error: {e}")
    
    # Test AIGenerationConfig model
    try:
        count = AIGenerationConfig.objects.count()
        print_success(f"AIGenerationConfig model accessible ({count} records)")
        tests_passed += 1
    except Exception as e:
        print_error(f"AIGenerationConfig model error: {e}")
    
    print_info(f"\nModels: {tests_passed}/3 tests passed")
    return tests_passed == 3


def test_environment_setup():
    """Test environment configuration."""
    print_header("TEST 5: Environment Setup")
    
    required_settings = [
        ('OPENAI_API_KEY', 'OpenAI API Key', False),
        ('ANTHROPIC_API_KEY', 'Anthropic API Key', False),
    ]
    
    optional_settings = [
        ('NEWSAPI_KEY', 'NewsAPI Key (for research agent)'),
        ('SERPER_API_KEY', 'Serper API Key (for web search)'),
        ('GPTZERO_API_KEY', 'GPTZero API Key (for AI detection)'),
    ]
    
    configured_count = 0
    
    print_info("Required API Keys:")
    for var_name, display_name, required in required_settings:
        if os.getenv(var_name):
            print_success(f"{display_name} configured")
            configured_count += 1
        else:
            print_error(f"{display_name} NOT configured")
            print_info(f"  Set with: export {var_name}='your-key-here'")
    
    print_info("\nOptional API Keys (for Phase 3):")
    for var_name, display_name in optional_settings:
        if os.getenv(var_name):
            print_success(f"{display_name} configured")
        else:
            print_info(f"{display_name} not configured (optional)")
    
    return configured_count >= 1  # At least OpenAI key


def main():
    """Run all Phase 2 tests."""
    print_header("🤖 PHASE 2 INTEGRATION TESTS")
    print_info(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'Dependencies': test_imports(),
        'Prompt Templates': test_prompt_templates(),
        'Orchestrator': test_orchestrator(),
        'Django Models': test_models(),
        'Environment': test_environment_setup(),
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
        print(f"{GREEN}✅ Phase 2 Implementation: SUCCESSFUL{RESET}")
        print(f"{GREEN}All {total} test categories passed!{RESET}")
        print(f"\n{YELLOW}Next Steps:{RESET}")
        print("1. Configure API keys if not already done:")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        print("\n2. Ready for Phase 3: Core Pipeline Tools")
        print("   - Keyword scraper")
        print("   - Research agent")
        print("   - Content generation chain")
        print("   - Quality control tools (bias, facts, plagiarism)")
        print("\n3. Or proceed to Phase 4: Celery Setup for async processing")
    else:
        print(f"{YELLOW}⚠️  Phase 2 Implementation: PARTIAL{RESET}")
        print(f"{passed}/{total} test categories passed")
        print(f"\n{YELLOW}Action Required:{RESET}")
        
        if not results['Dependencies']:
            print("• Install missing dependencies: pip install -r requirements.txt")
        if not results['Orchestrator'] or not results['Environment']:
            print("• Configure API keys (see above)")
        if not results['Django Models']:
            print("• Run migrations: python manage.py migrate")
    
    print(f"{BLUE}{'=' * 70}{RESET}\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
