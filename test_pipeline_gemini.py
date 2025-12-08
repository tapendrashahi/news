#!/usr/bin/env python
"""
Test AI Article Generation Pipeline with Gemini
Creates a complete article from keyword to final content
"""
import os
import sys
import django
import asyncio

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.ai_models import KeywordSource, AIArticle, AIGenerationConfig
from news.ai_pipeline.orchestrator import AINewsOrchestrator
from django.contrib.auth import get_user_model

User = get_user_model()


def create_test_keyword():
    """Create a test keyword for article generation"""
    print("\n📝 Creating test keyword...")
    
    # Get or create admin user
    try:
        user = User.objects.filter(is_staff=True).first()
        if not user:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("   Created admin user")
    except Exception as e:
        user = User.objects.first()
        print(f"   Using existing user: {user.username}")
    
    # Create keyword source
    keyword, created = KeywordSource.objects.get_or_create(
        keyword="AI-powered healthcare diagnostics revolution",
        defaults={
            'source': 'manual',
            'category': 'technology',
            'status': KeywordSource.Status.APPROVED,
            'priority': 8,
            'approved_by': user,
            'notes': 'Test keyword for Gemini integration'
        }
    )
    
    if created:
        print(f"   ✓ Created keyword: {keyword.keyword}")
    else:
        print(f"   ✓ Using existing keyword: {keyword.keyword}")
    
    return keyword, user


def test_basic_generation():
    """Test basic content generation without full pipeline"""
    print("\n" + "=" * 60)
    print("TEST: Basic Article Generation with Gemini")
    print("=" * 60)
    
    try:
        # Create test data
        keyword, user = create_test_keyword()
        
        # Create AI article
        print("\n📰 Creating AI Article...")
        article = AIArticle.objects.create(
            keyword=keyword,
            title=f"Test: {keyword.keyword}",  # Provide title to generate slug
            template_type=AIArticle.TemplateType.ANALYSIS,
            status=AIArticle.Status.QUEUED,
            target_word_count=800,
            ai_model_used='gemini-2.0-flash-exp'
        )
        print(f"   ✓ Article created: {article.id}")
        
        # Initialize orchestrator
        print("\n🤖 Initializing Gemini orchestrator...")
        orchestrator = AINewsOrchestrator()
        print(f"   ✓ Using model: {orchestrator.config['default_model']}")
        
        # Generate title and outline
        print("\n✍️  Generating article content...")
        article.status = AIArticle.Status.GENERATING
        article.workflow_stage = AIArticle.WorkflowStage.CONTENT_GENERATION
        article.save()
        
        from langchain.schema import HumanMessage, SystemMessage
        
        # Generate title
        title_messages = [
            SystemMessage(content="""You are a professional news headline writer. 
Create concise, engaging headlines that are factual and SEO-friendly.
Follow these rules:
- Keep it under 80 characters
- Make it specific and newsworthy
- Avoid clickbait
- Be clear and direct
- Return ONLY the headline, no explanations or options"""),
            HumanMessage(content=f"Write ONE compelling news headline about: {keyword.keyword}\n\nReturn only the headline:")
        ]
        
        title_response = orchestrator.llm_primary.invoke(title_messages)
        # Extract first line if multiple options given, truncate to 255 chars
        title_text = title_response.content.strip().split('\n')[0].strip().strip('"\'*-•')
        # Remove common prefixes like "Here are..." or numbers/bullets
        if ':' in title_text:
            title_text = title_text.split(':', 1)[-1].strip()
        article.title = title_text[:255]
        print(f"   📌 Title: {article.title}")
        
        # Generate outline
        outline_messages = [
            SystemMessage(content="""You are an expert news article planner.
Create a structured outline for news articles.
Return a JSON-like outline with sections and key points."""),
            HumanMessage(content=f"""Create a detailed outline for an {article.target_word_count}-word article about:
Topic: {keyword.keyword}
Template: {article.get_template_type_display()}

Include:
- Introduction hook
- 3-4 main sections
- Key points for each section
- Conclusion""")
        ]
        
        outline_response = orchestrator.llm_primary.invoke(outline_messages)
        article.outline = {'raw': outline_response.content}
        print(f"   📋 Outline generated ({len(outline_response.content)} chars)")
        
        # Generate main content
        content_messages = [
            SystemMessage(content=f"""You are a professional AI journalist writing for AI Analitica.

Mission: Provide unbiased, data-driven news analysis with multiple perspectives.

Standards:
- Write in clear, professional tone
- Include facts and data
- Present multiple viewpoints
- Avoid bias and sensationalism
- Target readability: Grade 10-12
- Word count: ~{article.target_word_count} words

Format: Write in markdown with proper headings (##, ###)"""),
            HumanMessage(content=f"""Write a complete news article:

Title: {article.title}
Topic: {keyword.keyword}
Category: {keyword.category.title()}

Outline:
{article.outline['raw'][:500]}...

Write the full article now.""")
        ]
        
        print("   🔄 Generating content (this may take 10-30 seconds)...")
        content_response = orchestrator.llm_primary.invoke(content_messages)
        article.raw_content = content_response.content
        article.actual_word_count = len(content_response.content.split())
        
        print(f"   ✅ Content generated: {article.actual_word_count} words")
        
        # Generate meta description
        meta_messages = [
            SystemMessage(content="Create SEO meta descriptions under 160 characters. Return ONLY the meta description, no explanations."),
            HumanMessage(content=f"Write ONE meta description for this article (max 160 chars):\n\nTitle: {article.title}\n\nReturn only the meta description:")
        ]
        
        meta_response = orchestrator.llm_primary.invoke(meta_messages)
        # Extract first line if multiple options, truncate to 160 chars
        meta_text = meta_response.content.strip().split('\n')[0].strip().strip('"\'*-•')
        if ':' in meta_text:
            meta_text = meta_text.split(':', 1)[-1].strip()
        article.meta_description = meta_text[:160]
        article.meta_title = article.title[:60]
        print(f"   🏷️  Meta description: {article.meta_description}")
        
        # Update status
        article.status = AIArticle.Status.REVIEWING
        article.workflow_stage = AIArticle.WorkflowStage.COMPLETED
        article.save()
        
        # Display results
        print("\n" + "=" * 60)
        print("✅ ARTICLE GENERATION COMPLETE")
        print("=" * 60)
        print(f"ID: {article.id}")
        print(f"Title: {article.title}")
        print(f"Slug: {article.slug}")
        print(f"Word Count: {article.actual_word_count}/{article.target_word_count}")
        print(f"Status: {article.get_status_display()}")
        print(f"Model: {article.ai_model_used}")
        print(f"\nMeta Description:\n{article.meta_description}")
        print(f"\nContent Preview (first 500 chars):")
        print("-" * 60)
        print(article.raw_content[:500])
        print("...")
        print("-" * 60)
        
        print(f"\n💾 View full article in admin: /admin/news/aiarticle/{article.id}/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run the test"""
    print("\n" + "🧪 " * 20)
    print("GEMINI PIPELINE TEST - Full Article Generation")
    print("🧪 " * 20)
    
    success = test_basic_generation()
    
    if success:
        print("\n🎉 Pipeline test successful!")
        print("✅ Gemini integration is fully functional")
        return 0
    else:
        print("\n⚠️  Pipeline test failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
