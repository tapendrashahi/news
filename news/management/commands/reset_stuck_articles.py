"""
Management command to reset stuck article generations.

Usage:
    python manage.py reset_stuck_articles
    python manage.py reset_stuck_articles --hours 2
    python manage.py reset_stuck_articles --article-id <uuid>
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from news.ai_models import AIArticle


class Command(BaseCommand):
    help = 'Reset stuck article generations (articles in "generating" status for too long)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=1,
            help='Reset articles stuck for more than this many hours (default: 1)'
        )
        parser.add_argument(
            '--article-id',
            type=str,
            help='Reset a specific article by UUID'
        )
        parser.add_argument(
            '--to-queued',
            action='store_true',
            help='Reset to QUEUED status instead of FAILED'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        article_id = options.get('article_id')
        to_queued = options['to_queued']
        
        if article_id:
            # Reset specific article
            try:
                article = AIArticle.objects.get(id=article_id)
                self.reset_article(article, to_queued)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Reset article {article_id}')
                )
            except AIArticle.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Article {article_id} not found')
                )
            return
        
        # Reset stuck articles
        time_threshold = timezone.now() - timedelta(hours=hours)
        stuck_articles = AIArticle.objects.filter(
            status='generating',
            updated_at__lt=time_threshold
        )
        
        count = stuck_articles.count()
        
        if count == 0:
            self.stdout.write(
                self.style.WARNING(f'No stuck articles found (stuck > {hours} hours)')
            )
            return
        
        self.stdout.write(f'Found {count} stuck article(s)')
        
        for article in stuck_articles:
            self.stdout.write(f'\nResetting: {article.keyword.keyword}')
            self.stdout.write(f'  ID: {article.id}')
            self.stdout.write(f'  Was stuck at: {article.workflow_stage}')
            self.stdout.write(f'  Last updated: {article.updated_at}')
            
            self.reset_article(article, to_queued)
        
        new_status = 'QUEUED' if to_queued else 'FAILED'
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Reset {count} article(s) to {new_status} status')
        )
    
    def reset_article(self, article, to_queued=False):
        """Reset a single article."""
        if to_queued:
            article.status = AIArticle.Status.QUEUED
            article.workflow_stage = AIArticle.WorkflowStage.KEYWORD_ANALYSIS
            article.last_error = ""
            article.failed_stage = ""
        else:
            article.status = AIArticle.Status.FAILED
            article.last_error = (
                f"Generation stuck at {article.workflow_stage} stage. "
                f"Process timed out or crashed. Please retry."
            )
            article.failed_stage = article.workflow_stage
        
        article.save()
