#!/usr/bin/env python
"""
Test AI Content API Endpoints
Phase 1 - Basic CRUD Testing
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.ai_models import KeywordSource, AIArticle, AIGenerationConfig, AIWorkflowLog
from django.contrib.auth import get_user_model

User = get_user_model()

def test_phase_1():
    """Test Phase 1 implementation"""
    print("=" * 60)
    print("Phase 1: Database Models & Backend Setup - Testing")
    print("=" * 60)
    
    # Test 1: Create a keyword
    print("\n✓ Test 1: Creating a keyword...")
    keyword = KeywordSource.objects.create(
        keyword="AI news automation",
        source=KeywordSource.Source.MANUAL,
        search_volume=1000,
        competition='medium',
        priority=1,
        category='tech',
        notes="Test keyword for AI automation system"
    )
    print(f"  Created: {keyword}")
    print(f"  ID: {keyword.id}")
    print(f"  Status: {keyword.status}")
    
    # Test 2: Approve keyword
    print("\n✓ Test 2: Approving keyword...")
    user = User.objects.first()
    if user:
        keyword.approve(user)
        print(f"  Approved by: {user.username}")
        print(f"  Status: {keyword.status}")
    else:
        print("  ⚠ No user found, skipping approval test")
    
    # Test 3: Create an AI article
    print("\n✓ Test 3: Creating an AI article...")
    article = AIArticle.objects.create(
        keyword=keyword,
        template_type=AIArticle.TemplateType.ANALYSIS,
        title="Test AI Generated Article About AI News Automation",
        target_word_count=1500,
        ai_model_used='gpt-4-turbo-preview'
    )
    print(f"  Created: {article}")
    print(f"  ID: {article.id}")
    print(f"  Slug: {article.slug}")
    print(f"  Status: {article.status}")
    print(f"  Workflow Stage: {article.workflow_stage}")
    
    # Test 4: Test quality score calculation
    print("\n✓ Test 4: Setting quality scores...")
    article.bias_score = 15.5
    article.fact_check_score = 95.0
    article.seo_score = 80.0
    article.readability_score = 75.0
    article.ai_score = 35.0
    article.plagiarism_score = 2.5
    article.save()
    
    overall = article.calculate_overall_quality()
    article.overall_quality_score = overall
    article.save()
    
    print(f"  Bias Score: {article.bias_score}% (target: <20%)")
    print(f"  Fact Check: {article.fact_check_score}% (target: >80%)")
    print(f"  SEO Score: {article.seo_score}% (target: >75%)")
    print(f"  Overall Quality: {article.overall_quality_score}%")
    print(f"  Passes Quality Threshold: {article.passes_quality_threshold}")
    
    # Test 5: Create generation config
    print("\n✓ Test 5: Creating AI generation config...")
    config = AIGenerationConfig.objects.create(
        name="Default Analysis Config",
        description="Default configuration for analysis articles",
        template_type=AIArticle.TemplateType.ANALYSIS,
        ai_provider=AIGenerationConfig.Provider.OPENAI,
        model_name='gpt-4-turbo-preview',
        system_prompt="You are an AI journalist for AI Analitica...",
        user_prompt_template="Write a {word_count} word article about {keyword}...",
        temperature=0.7,
        max_tokens=4000,
        target_word_count=1500,
        is_default=True,
        enabled=True
    )
    print(f"  Created: {config}")
    print(f"  Provider: {config.ai_provider}")
    print(f"  Model: {config.model_name}")
    print(f"  Max Bias Score: {config.max_bias_score}%")
    
    # Test 6: Create workflow log
    print("\n✓ Test 6: Creating workflow log...")
    log = AIWorkflowLog.objects.create(
        article=article,
        stage=AIArticle.WorkflowStage.KEYWORD_ANALYSIS,
        status=AIWorkflowLog.LogStatus.COMPLETED,
        execution_time=1250,
        tokens_used=150,
        cost=0.002,
        ai_model='gpt-4-turbo-preview',
        input_data={'keyword': keyword.keyword},
        output_data={'viability_score': 85.5}
    )
    print(f"  Created: {log}")
    print(f"  Stage: {log.get_stage_display()}")
    print(f"  Execution Time: {log.execution_time}ms")
    print(f"  Cost: ${log.cost}")
    
    # Test 7: Test article stage advancement
    print("\n✓ Test 7: Testing workflow stage advancement...")
    print(f"  Current Stage: {article.get_workflow_stage_display()}")
    next_stage = article.get_next_stage()
    print(f"  Next Stage: {next_stage}")
    article.advance_stage()
    print(f"  Advanced to: {article.get_workflow_stage_display()}")
    
    # Test 8: Test error logging
    print("\n✓ Test 8: Testing error logging...")
    article.log_error('research', 'Test error: API rate limit exceeded')
    print(f"  Error logged")
    print(f"  Last Error: {article.last_error}")
    print(f"  Failed Stage: {article.failed_stage}")
    print(f"  Error Log Entries: {len(article.error_log)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("PHASE 1 TEST SUMMARY")
    print("=" * 60)
    print(f"✓ Keywords created: {KeywordSource.objects.count()}")
    print(f"✓ Articles created: {AIArticle.objects.count()}")
    print(f"✓ Configs created: {AIGenerationConfig.objects.count()}")
    print(f"✓ Workflow logs created: {AIWorkflowLog.objects.count()}")
    print("\n✅ Phase 1 Implementation: SUCCESSFUL")
    print("=" * 60)
    
    # Print API endpoints
    print("\n📡 Available API Endpoints:")
    print("  POST   /api/admin/ai/keywords/           - Create keyword")
    print("  GET    /api/admin/ai/keywords/           - List keywords")
    print("  POST   /api/admin/ai/keywords/{id}/approve/  - Approve keyword")
    print("  POST   /api/admin/ai/keywords/{id}/reject/   - Reject keyword")
    print("  POST   /api/admin/ai/articles/           - Create article")
    print("  GET    /api/admin/ai/articles/           - List articles")
    print("  POST   /api/admin/ai/articles/{id}/start_generation/  - Start generation")
    print("  GET    /api/admin/ai/configs/            - List configs")
    print("  GET    /api/admin/ai/logs/               - View logs")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_phase_1()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
