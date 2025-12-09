#!/usr/bin/env python
"""
Manual pipeline runner for stuck articles
Usage: python run_pipeline_manual.py <article_id>
"""
import os
import sys
import django
import asyncio

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')
django.setup()

from news.ai_models import AIArticle
from news.ai_pipeline.orchestrator import AINewsOrchestrator

def run_pipeline(article_id):
    try:
        article = AIArticle.objects.get(id=article_id)
        print(f'📰 Article: {article.keyword.keyword if article.keyword else "Unknown"}')
        print(f'   Status: {article.status}')
        print(f'   Stage: {article.workflow_stage}')
        print(f'   Created: {article.created_at}')
        
        if article.status not in ['queued', 'generating', 'failed']:
            print(f'\n⚠️  Article status is "{article.status}" - not suitable for generation')
            return
        
        # Update status to generating
        article.status = 'generating'
        article.workflow_stage = 'keyword_analysis'
        article.save()
        
        print('\n🚀 Starting pipeline...\n')
        orchestrator = AINewsOrchestrator()  # Use default config
        result = asyncio.run(orchestrator.process_article(article_id=article_id))
        
        # Refresh article
        article.refresh_from_db()
        
        print(f'\n✅ Pipeline completed!')
        print(f'   Title: {article.title or "N/A"}')
        print(f'   Status: {article.status}')
        print(f'   Stage: {article.workflow_stage}')
        print(f'   Word Count: {article.word_count or 0}')
        
    except AIArticle.DoesNotExist:
        print(f'❌ Article {article_id} not found')
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python run_pipeline_manual.py <article_id>')
        print('\nStuck articles:')
        stuck = AIArticle.objects.filter(status='generating').order_by('-created_at')[:5]
        for a in stuck:
            print(f'  {a.id} - {a.keyword.keyword if a.keyword else "Unknown"} ({a.workflow_stage})')
        sys.exit(1)
    
    article_id = sys.argv[1]
    run_pipeline(article_id)
