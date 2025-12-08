"""
Celery Tasks for AI Content Generation

Task 4.1: Celery Setup Implementation
- @shared_task generate_article_pipeline(ai_article_id)
- @shared_task process_keyword_batch(keyword_ids)
- @shared_task retry_failed_stage(ai_article_id, stage)
- Task progress tracking
- Error handling and retries
"""

import logging
from celery import shared_task
from decimal import Decimal
from typing import Dict, Any
import asyncio

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_article_async(self, article_id: str) -> Dict[str, Any]:
    """
    Async task to generate an AI article through the complete pipeline.
    
    Args:
        article_id: UUID of the AIArticle to process
        
    Returns:
        Dictionary with generation results
    """
    from news.ai_models import AIArticle
    from news.ai_pipeline.orchestrator import AINewsOrchestrator
    
    try:
        logger.info(f"Starting article generation for {article_id}")
        
        # Update article status
        article = AIArticle.objects.get(id=article_id)
        article.status = 'generating'
        article.workflow_stage = 'keyword_analysis'
        article.save()
        
        # Initialize orchestrator
        orchestrator = AINewsOrchestrator()
        
        # Run the pipeline (async function needs event loop)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                orchestrator.process_article(article_id)
            )
        finally:
            loop.close()
        
        logger.info(f"Article generation completed for {article_id}")
        return result
        
    except Exception as exc:
        logger.error(f"Article generation failed for {article_id}: {exc}")
        
        # Update article status
        try:
            article = AIArticle.objects.get(id=article_id)
            article.status = 'failed'
            article.error_log = str(exc)
            article.save()
        except Exception as e:
            logger.error(f"Failed to update article status: {e}")
        
        # Retry the task
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def retry_article_stage(self, article_id: str, failed_stage: str) -> Dict[str, Any]:
    """
    Retry article generation from a specific failed stage.
    
    Args:
        article_id: UUID of the AIArticle
        failed_stage: Stage name where failure occurred
        
    Returns:
        Dictionary with retry results
    """
    from news.ai_models import AIArticle
    from news.ai_pipeline.orchestrator import AINewsOrchestrator
    
    try:
        logger.info(f"Retrying article {article_id} from stage {failed_stage}")
        
        article = AIArticle.objects.get(id=article_id)
        article.status = 'generating'
        article.workflow_stage = failed_stage
        article.retry_count += 1
        article.save()
        
        orchestrator = AINewsOrchestrator()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                orchestrator.retry_article(article_id, failed_stage)
            )
        finally:
            loop.close()
        
        logger.info(f"Article retry completed for {article_id}")
        return result
        
    except Exception as exc:
        logger.error(f"Article retry failed for {article_id}: {exc}")
        raise self.retry(exc=exc)


@shared_task
def run_quality_checks(article_id: str) -> Dict[str, Any]:
    """
    Run all quality checks on generated content.
    
    Args:
        article_id: UUID of the AIArticle
        
    Returns:
        Dictionary with quality scores
    """
    from news.ai_models import AIArticle
    from news.ai_pipeline.tools.bias_detector import BiasDetectionTool
    from news.ai_pipeline.tools.fact_verifier import FactVerificationTool
    from news.ai_pipeline.tools.perspective_analyzer import PerspectiveAnalyzer
    
    try:
        logger.info(f"Running quality checks for {article_id}")
        
        article = AIArticle.objects.get(id=article_id)
        content = article.raw_content or ""
        title = article.title or ""
        
        # Initialize tools
        bias_detector = BiasDetectionTool()
        fact_verifier = FactVerificationTool()
        perspective_analyzer = PerspectiveAnalyzer()
        
        # Run checks
        bias_result = bias_detector.detect_bias(content, title)
        fact_result = fact_verifier.verify_facts(content, title)
        perspective_result = perspective_analyzer.analyze_perspectives(
            content,
            article.keyword.keyword if article.keyword else ""
        )
        
        # Update article scores
        article.bias_score = Decimal(str(bias_result['bias_score']))
        article.fact_check_score = Decimal(str(fact_result['verification_score']))
        article.perspective_balance_score = Decimal(str(perspective_result['balance_score']))
        
        # Calculate overall quality
        article.calculate_overall_quality()
        article.save()
        
        logger.info(f"Quality checks completed for {article_id}")
        
        return {
            'article_id': article_id,
            'bias_score': float(article.bias_score),
            'fact_check_score': float(article.fact_check_score),
            'perspective_balance_score': float(article.perspective_balance_score),
            'overall_quality': float(article.overall_quality_score),
            'passes_standards': (
                bias_result['passes_threshold'] and
                fact_result['passes_threshold'] and
                perspective_result['passes_threshold']
            )
        }
        
    except Exception as exc:
        logger.error(f"Quality checks failed for {article_id}: {exc}")
        raise


@shared_task
def batch_generate_articles(keyword_ids: list) -> Dict[str, Any]:
    """
    Generate multiple articles in batch from approved keywords.
    
    Args:
        keyword_ids: List of KeywordSource UUIDs
        
    Returns:
        Dictionary with batch generation results
    """
    from news.ai_models import KeywordSource, AIArticle
    
    try:
        logger.info(f"Batch generating {len(keyword_ids)} articles")
        
        results = {
            'total': len(keyword_ids),
            'created': 0,
            'failed': 0,
            'article_ids': []
        }
        
        for keyword_id in keyword_ids:
            try:
                keyword = KeywordSource.objects.get(id=keyword_id)
                
                # Create article
                article = AIArticle.objects.create(
                    keyword=keyword,
                    template_type='analysis',
                    status='queued'
                )
                
                # Queue for generation
                generate_article_async.delay(str(article.id))
                
                results['created'] += 1
                results['article_ids'].append(str(article.id))
                
            except Exception as e:
                logger.error(f"Failed to create article for keyword {keyword_id}: {e}")
                results['failed'] += 1
        
        logger.info(f"Batch generation queued: {results['created']} created")
        return results
        
    except Exception as exc:
        logger.error(f"Batch generation failed: {exc}")
        raise
