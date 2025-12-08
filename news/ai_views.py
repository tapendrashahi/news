"""
AI Content API Views

Task 1.3: API Views Implementation
- KeywordSourceViewSet (CRUD + approve/reject actions)
- AIArticleViewSet (CRUD + retry/cancel/publish actions)
- AIGenerationConfigViewSet (CRUD for configs)
- AIWorkflowLogViewSet (read-only logs)
- Custom actions: start_generation, retry_stage, cancel_generation
"""

"""
AI Content Generation API Views

Task 1.3: API Views Implementation
- KeywordSourceViewSet (CRUD + approve/reject actions)
- AIArticleViewSet (CRUD + retry/cancel/publish actions)
- AIGenerationConfigViewSet (CRUD for configs)
- AIWorkflowLogViewSet (read-only logs)
"""

from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger(__name__)

from .ai_models import (
    KeywordSource,
    AIArticle,
    AIGenerationConfig,
    AIWorkflowLog,
    NewsSourceConfig,
    ScrapedArticle
)
from .ai_serializers import (
    KeywordSourceSerializer,
    KeywordSourceListSerializer,
    AIArticleSerializer,
    AIArticleListSerializer,
    AIArticleDetailSerializer,
    AIGenerationConfigSerializer,
    AIWorkflowLogSerializer,
    NewsSourceConfigSerializer,
    ScrapedArticleSerializer,
    ScrapedArticleListSerializer
)

# Import Celery task (will be created in Phase 4)
# from .ai_tasks import generate_article_pipeline, retry_failed_stage


# ============================================================================
# Keyword Source ViewSet
# ============================================================================

class KeywordSourceViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing keyword sources.
    
    Endpoints:
    - GET /api/keywords/ - List all keywords
    - POST /api/keywords/ - Create new keyword
    - GET /api/keywords/{id}/ - Get keyword details
    - PUT/PATCH /api/keywords/{id}/ - Update keyword
    - DELETE /api/keywords/{id}/ - Delete keyword
    - POST /api/keywords/{id}/approve/ - Approve keyword
    - POST /api/keywords/{id}/reject/ - Reject keyword
    - POST /api/keywords/bulk_approve/ - Bulk approve keywords
    - POST /api/keywords/bulk_reject/ - Bulk reject keywords
    - POST /api/keywords/{id}/generate_article/ - Generate article from keyword
    """
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'source', 'category', 'priority']
    search_fields = ['keyword', 'notes']
    ordering_fields = ['created_at', 'priority', 'search_volume', 'viability_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get keywords with optional filtering."""
        queryset = KeywordSource.objects.select_related(
            'approved_by'
        ).prefetch_related('articles')
        
        # Filter by status if provided in query params
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail views."""
        if self.action == 'list':
            return KeywordSourceListSerializer
        return KeywordSourceSerializer
    
    def perform_create(self, serializer):
        """Create keyword with additional processing."""
        keyword = serializer.save()
        
        # TODO: Trigger AI analysis for keyword viability
        # This would use LangChain to analyze the keyword
        # and populate suggested_angles, related_keywords, etc.
        
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve a keyword for article generation.
        
        POST /api/keywords/{id}/approve/
        """
        keyword = self.get_object()
        
        if keyword.status == KeywordSource.Status.APPROVED:
            return Response(
                {'detail': 'Keyword is already approved.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        keyword.approve(request.user)
        
        # Optionally auto-queue for generation
        auto_generate = request.data.get('auto_generate', True)
        if auto_generate:
            article = AIArticle.objects.create(
                keyword=keyword,
                status=AIArticle.Status.QUEUED,
                template_type=keyword.suggested_template or AIArticle.TemplateType.ANALYSIS
            )
            
            # TODO: Trigger async generation task
            # generate_article_pipeline.delay(str(article.id))
            
            return Response({
                'detail': 'Keyword approved and article generation queued.',
                'article_id': str(article.id)
            })
        
        return Response({'detail': 'Keyword approved successfully.'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a keyword.
        
        POST /api/keywords/{id}/reject/
        Body: {"reason": "Not relevant to our audience"}
        """
        keyword = self.get_object()
        reason = request.data.get('reason', '')
        
        if not reason:
            return Response(
                {'detail': 'Rejection reason is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        keyword.reject(request.user, reason)
        
        return Response({'detail': 'Keyword rejected.'})
    
    @action(detail=False, methods=['post'])
    def bulk_approve(self, request):
        """
        Bulk approve multiple keywords.
        
        POST /api/keywords/bulk_approve/
        Body: {"keyword_ids": ["uuid1", "uuid2"], "auto_generate": true}
        """
        keyword_ids = request.data.get('keyword_ids', [])
        auto_generate = request.data.get('auto_generate', True)
        
        if not keyword_ids:
            return Response(
                {'detail': 'No keyword IDs provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        keywords = KeywordSource.objects.filter(
            id__in=keyword_ids,
            status=KeywordSource.Status.PENDING
        )
        
        approved_count = 0
        article_ids = []
        
        for keyword in keywords:
            keyword.approve(request.user)
            approved_count += 1
            
            if auto_generate:
                article = AIArticle.objects.create(
                    keyword=keyword,
                    status=AIArticle.Status.QUEUED,
                    template_type=keyword.suggested_template or AIArticle.TemplateType.ANALYSIS
                )
                article_ids.append(str(article.id))
                # TODO: generate_article_pipeline.delay(str(article.id))
        
        return Response({
            'detail': f'{approved_count} keywords approved.',
            'approved_count': approved_count,
            'article_ids': article_ids
        })
    
    @action(detail=False, methods=['post'])
    def bulk_reject(self, request):
        """
        Bulk reject multiple keywords.
        
        POST /api/keywords/bulk_reject/
        Body: {"keyword_ids": ["uuid1", "uuid2"], "reason": "Not relevant"}
        """
        keyword_ids = request.data.get('keyword_ids', [])
        reason = request.data.get('reason', '')
        
        if not keyword_ids or not reason:
            return Response(
                {'detail': 'Keyword IDs and reason are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        keywords = KeywordSource.objects.filter(
            id__in=keyword_ids,
            status=KeywordSource.Status.PENDING
        )
        
        rejected_count = 0
        for keyword in keywords:
            keyword.reject(request.user, reason)
            rejected_count += 1
        
        return Response({
            'detail': f'{rejected_count} keywords rejected.',
            'rejected_count': rejected_count
        })
    
    @action(detail=True, methods=['post'])
    def generate_article(self, request, pk=None):
        """
        Manually trigger article generation for this keyword.
        
        POST /api/keywords/{id}/generate_article/
        Body: {"template_type": "analysis", "target_word_count": 1500}
        """
        keyword = self.get_object()
        
        if keyword.status != KeywordSource.Status.APPROVED:
            return Response(
                {'detail': 'Keyword must be approved before generating article.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if there's already a pending/generating article
        existing = AIArticle.objects.filter(
            keyword=keyword,
            status__in=[AIArticle.Status.QUEUED, AIArticle.Status.GENERATING]
        ).first()
        
        if existing:
            return Response(
                {'detail': 'Article generation already in progress for this keyword.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new article
        template_type = request.data.get('template_type', keyword.suggested_template or AIArticle.TemplateType.ANALYSIS)
        target_word_count = request.data.get('target_word_count', 1500)
        
        article = AIArticle.objects.create(
            keyword=keyword,
            status=AIArticle.Status.QUEUED,
            template_type=template_type,
            target_word_count=target_word_count
        )
        
        # TODO: Trigger async generation
        # generate_article_pipeline.delay(str(article.id))
        
        return Response({
            'detail': 'Article generation started.',
            'article_id': str(article.id)
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get keyword statistics.
        
        GET /api/keywords/statistics/
        """
        total = KeywordSource.objects.count()
        pending = KeywordSource.objects.filter(status=KeywordSource.Status.PENDING).count()
        approved = KeywordSource.objects.filter(status=KeywordSource.Status.APPROVED).count()
        rejected = KeywordSource.objects.filter(status=KeywordSource.Status.REJECTED).count()
        
        by_source = KeywordSource.objects.values('source').annotate(count=Count('id'))
        by_category = KeywordSource.objects.filter(
            category__isnull=False
        ).values('category__name').annotate(count=Count('id'))
        
        return Response({
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'by_source': list(by_source),
            'by_category': list(by_category),
            'average_viability': KeywordSource.objects.filter(
                viability_score__isnull=False
            ).aggregate(avg=Avg('viability_score'))['avg']
        })


# ============================================================================
# AI Article ViewSet
# ============================================================================

class AIArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing AI-generated articles.
    
    Endpoints:
    - GET /api/ai-articles/ - List all articles
    - POST /api/ai-articles/ - Create new article (manual trigger)
    - GET /api/ai-articles/{id}/ - Get article details
    - PUT/PATCH /api/ai-articles/{id}/ - Update article
    - DELETE /api/ai-articles/{id}/ - Delete article
    - POST /api/ai-articles/{id}/retry/ - Retry failed generation
    - POST /api/ai-articles/{id}/retry_stage/ - Retry specific stage
    - POST /api/ai-articles/{id}/cancel/ - Cancel generation
    - POST /api/ai-articles/{id}/approve/ - Approve for publishing
    - POST /api/ai-articles/{id}/reject/ - Reject article
    - POST /api/ai-articles/{id}/publish/ - Publish to live site
    - GET /api/ai-articles/queue/ - Get generation queue
    - GET /api/ai-articles/review_queue/ - Get review queue
    """
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'workflow_stage', 'template_type', 'keyword__category']
    search_fields = ['title', 'keyword__keyword']
    ordering_fields = ['created_at', 'generation_time', 'overall_quality_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get articles with related data."""
        queryset = AIArticle.objects.select_related(
            'keyword', 'keyword__category', 'reviewed_by', 'published_article'
        ).prefetch_related('workflow_logs')
        
        return queryset
    
    def get_serializer_class(self):
        """Use different serializers based on action."""
        if self.action == 'list':
            return AIArticleListSerializer
        elif self.action == 'retrieve':
            return AIArticleDetailSerializer
        return AIArticleSerializer
    
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """
        Retry article generation from the beginning.
        
        POST /api/ai-articles/{id}/retry/
        """
        article = self.get_object()
        
        if article.status not in [AIArticle.Status.FAILED, AIArticle.Status.REJECTED]:
            return Response(
                {'detail': 'Can only retry failed or rejected articles.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reset article state
        article.status = AIArticle.Status.QUEUED
        article.workflow_stage = AIArticle.WorkflowStage.KEYWORD_ANALYSIS
        article.retry_count += 1
        article.last_error = ''
        article.failed_stage = ''
        article.generation_started_at = None
        article.generation_completed_at = None
        article.save()
        
        # TODO: Trigger async generation
        # generate_article_pipeline.delay(str(article.id))
        
        return Response({
            'detail': 'Article generation restarted.',
            'retry_count': article.retry_count
        })
    
    @action(detail=True, methods=['post'])
    def retry_stage(self, request, pk=None):
        """
        Retry a specific failed stage.
        
        POST /api/ai-articles/{id}/retry_stage/
        Body: {"stage": "content_generation"}
        """
        article = self.get_object()
        stage = request.data.get('stage')
        
        if not stage:
            return Response(
                {'detail': 'Stage is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if stage not in AIArticle.WorkflowStage.values:
            return Response(
                {'detail': f'Invalid stage: {stage}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reset to specified stage
        article.workflow_stage = stage
        article.status = AIArticle.Status.GENERATING
        article.retry_count += 1
        article.save()
        
        # TODO: Trigger async stage retry
        # retry_failed_stage.delay(str(article.id), stage)
        
        return Response({
            'detail': f'Retrying stage: {stage}',
            'current_stage': article.workflow_stage
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel ongoing article generation.
        
        POST /api/ai-articles/{id}/cancel/
        """
        article = self.get_object()
        
        if article.status not in [AIArticle.Status.QUEUED, AIArticle.Status.GENERATING]:
            return Response(
                {'detail': 'Can only cancel queued or generating articles.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        article.status = AIArticle.Status.FAILED
        article.last_error = 'Cancelled by user'
        article.save()
        
        # TODO: Cancel Celery task if possible
        
        return Response({'detail': 'Article generation cancelled.'})
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve article for publishing.
        
        POST /api/ai-articles/{id}/approve/
        Body: {"notes": "Looks good"}
        """
        article = self.get_object()
        
        if article.status != AIArticle.Status.REVIEWING:
            return Response(
                {'detail': 'Article must be in review status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        article.status = AIArticle.Status.APPROVED
        article.reviewed_by = request.user
        article.review_notes = request.data.get('notes', '')
        article.save()
        
        return Response({
            'detail': 'Article approved.',
            'can_publish': True
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject article and optionally request regeneration.
        
        POST /api/ai-articles/{id}/reject/
        Body: {"notes": "Needs more data", "regenerate": true}
        """
        article = self.get_object()
        notes = request.data.get('notes', '')
        regenerate = request.data.get('regenerate', False)
        
        if not notes:
            return Response(
                {'detail': 'Rejection notes are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        article.status = AIArticle.Status.REJECTED
        article.reviewed_by = request.user
        article.review_notes = notes
        article.save()
        
        if regenerate:
            # Create new article for regeneration
            new_article = AIArticle.objects.create(
                keyword=article.keyword,
                status=AIArticle.Status.QUEUED,
                template_type=article.template_type,
                target_word_count=article.target_word_count
            )
            # TODO: generate_article_pipeline.delay(str(new_article.id))
            
            return Response({
                'detail': 'Article rejected. New generation started.',
                'new_article_id': str(new_article.id)
            })
        
        return Response({'detail': 'Article rejected.'})
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Publish article to live site.
        
        POST /api/ai-articles/{id}/publish/
        Body: {"visibility": "public"}
        """
        article = self.get_object()
        
        if article.status != AIArticle.Status.APPROVED:
            return Response(
                {'detail': 'Article must be approved before publishing.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if article.published_article:
            return Response(
                {'detail': 'Article is already published.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Import News model
        from .models import News
        
        # Create published article
        visibility = request.data.get('visibility', 'public')
        
        news = News.objects.create(
            title=article.title,
            slug=article.slug,
            content=article.raw_content,
            excerpt=article.meta_description[:200] if article.meta_description else '',
            category=article.keyword.category,
            author=request.user,
            meta_description=article.meta_description,
            meta_title=article.meta_title,
            visibility=visibility,
            image=article.image_local_path or article.image_url
        )
        
        # Add tags
        if article.focus_keywords:
            # Assuming Tag model exists
            # for keyword in article.focus_keywords:
            #     tag, _ = Tag.objects.get_or_create(name=keyword)
            #     news.tags.add(tag)
            pass
        
        # Link to AI article
        article.published_article = news
        article.status = AIArticle.Status.PUBLISHED
        article.published_at = timezone.now()
        article.save()
        
        return Response({
            'detail': 'Article published successfully.',
            'article_id': news.id,
            'article_url': f'/news/{news.slug}/'
        })
    
    @action(detail=False, methods=['get'])
    def queue(self, request):
        """
        Get current generation queue.
        
        GET /api/ai-articles/queue/
        Returns articles that are queued or currently generating.
        """
        articles = self.get_queryset().filter(
            status__in=[AIArticle.Status.QUEUED, AIArticle.Status.GENERATING]
        ).order_by('created_at')
        
        serializer = AIArticleListSerializer(articles, many=True)
        return Response({
            'count': articles.count(),
            'articles': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def review_queue(self, request):
        """
        Get articles ready for review.
        
        GET /api/ai-articles/review_queue/
        Returns completed articles awaiting human review.
        """
        articles = self.get_queryset().filter(
            status=AIArticle.Status.REVIEWING,
            workflow_stage=AIArticle.WorkflowStage.COMPLETED
        ).order_by('generation_completed_at')
        
        serializer = AIArticleListSerializer(articles, many=True)
        return Response({
            'count': articles.count(),
            'articles': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get article generation statistics.
        
        GET /api/ai-articles/statistics/
        """
        total = AIArticle.objects.count()
        by_status = AIArticle.objects.values('status').annotate(count=Count('id'))
        by_stage = AIArticle.objects.values('workflow_stage').annotate(count=Count('id'))
        
        # Quality metrics
        quality_stats = AIArticle.objects.filter(
            overall_quality_score__isnull=False
        ).aggregate(
            avg_quality=Avg('overall_quality_score'),
            avg_bias=Avg('bias_score'),
            avg_seo=Avg('seo_score'),
            avg_readability=Avg('readability_score')
        )
        
        # Performance metrics
        performance = AIArticle.objects.filter(
            generation_time__isnull=False
        ).aggregate(
            avg_time=Avg('generation_time'),
            total_cost=Avg('cost_estimate')
        )
        
        # Success rate
        completed = AIArticle.objects.filter(
            status__in=[AIArticle.Status.APPROVED, AIArticle.Status.PUBLISHED]
        ).count()
        success_rate = (completed / total * 100) if total > 0 else 0
        
        return Response({
            'total': total,
            'by_status': list(by_status),
            'by_stage': list(by_stage),
            'quality_metrics': quality_stats,
            'performance': performance,
            'success_rate': round(success_rate, 2)
        })


# ============================================================================
# AI Generation Config ViewSet
# ============================================================================

class AIGenerationConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing AI generation configurations.
    
    Endpoints:
    - GET /api/ai-configs/ - List all configs
    - POST /api/ai-configs/ - Create new config
    - GET /api/ai-configs/{id}/ - Get config details
    - PUT/PATCH /api/ai-configs/{id}/ - Update config
    - DELETE /api/ai-configs/{id}/ - Delete config
    - POST /api/ai-configs/{id}/set_default/ - Set as default config
    - POST /api/ai-configs/{id}/duplicate/ - Duplicate config
    """
    
    queryset = AIGenerationConfig.objects.all()
    serializer_class = AIGenerationConfigSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['template_type', 'ai_provider', 'enabled', 'is_default']
    search_fields = ['name', 'description']
    ordering = ['-is_default', 'name']
    
    def perform_create(self, serializer):
        """Set created_by user on create."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """
        Set this config as the default for its template type.
        
        POST /api/ai-configs/{id}/set_default/
        """
        config = self.get_object()
        
        # Unset other defaults for this template type
        AIGenerationConfig.objects.filter(
            template_type=config.template_type,
            is_default=True
        ).exclude(pk=config.pk).update(is_default=False)
        
        config.is_default = True
        config.save()
        
        return Response({'detail': f'{config.name} is now the default config.'})
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Duplicate an existing config.
        
        POST /api/ai-configs/{id}/duplicate/
        Body: {"name": "New Config Name"}
        """
        config = self.get_object()
        new_name = request.data.get('name')
        
        if not new_name:
            new_name = f"{config.name} (Copy)"
        
        # Create duplicate
        config.pk = None
        config.id = None
        config.name = new_name
        config.is_default = False
        config.version = 1
        config.created_by = request.user
        config.save()
        
        serializer = self.get_serializer(config)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ============================================================================
# AI Workflow Log ViewSet
# ============================================================================

class AIWorkflowLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for viewing workflow logs.
    
    Endpoints:
    - GET /api/workflow-logs/ - List all logs
    - GET /api/workflow-logs/{id}/ - Get log details
    - GET /api/workflow-logs/article/{article_id}/ - Get logs for specific article
    """
    
    queryset = AIWorkflowLog.objects.select_related('article').all()
    serializer_class = AIWorkflowLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['article', 'stage', 'status']
    ordering = ['-timestamp']
    
    @action(detail=False, methods=['get'], url_path='article/(?P<article_id>[^/.]+)')
    def article_logs(self, request, article_id=None):
        """
        Get all logs for a specific article.
        
        GET /api/workflow-logs/article/{article_id}/
        """
        logs = self.get_queryset().filter(article_id=article_id)
        serializer = self.get_serializer(logs, many=True)
        
        # Calculate total execution time and cost
        total_time = sum(log.execution_time for log in logs)
        total_cost = sum(log.cost for log in logs)
        
        return Response({
            'article_id': article_id,
            'total_logs': logs.count(),
            'total_execution_time': total_time,
            'total_cost': float(total_cost),
            'logs': serializer.data
        })


# ============================================================================
# News Source Config ViewSet
# ============================================================================

class NewsSourceConfigViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing news source configurations.
    Setup keywords and target websites for scraping.
    """
    
    queryset = NewsSourceConfig.objects.all()
    serializer_class = NewsSourceConfigSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'keywords']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set created_by to current user."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def trigger_scrape(self, request, pk=None):
        """
        Manually trigger scraping for this configuration.
        
        POST /api/news-sources/{id}/trigger_scrape/
        """
        config = self.get_object()
        
        try:
            from .scraping_utils import scrape_articles_for_config
            
            # Scrape articles from configured websites
            scraped_data = scrape_articles_for_config(config)
            
            # Create ScrapedArticle records
            created_count = 0
            for article_data in scraped_data:
                try:
                    # Check if article already exists (by URL)
                    if not ScrapedArticle.objects.filter(source_url=article_data['source_url']).exists():
                        ScrapedArticle.objects.create(
                            source_config=config,
                            **article_data
                        )
                        created_count += 1
                except Exception as e:
                    logger.error(f"Error saving article: {str(e)}")
                    continue
            
            # Update last scraped timestamp
            config.last_scraped_at = timezone.now()
            config.save(update_fields=['last_scraped_at'])
            
            return Response({
                'detail': f'Scraping completed! Found and saved {created_count} new articles.',
                'config_id': str(config.id),
                'config_name': config.name,
                'articles_created': created_count,
                'total_found': len(scraped_data)
            })
            
        except Exception as e:
            logger.error(f"Scraping error: {str(e)}")
            return Response({
                'detail': f'Scraping failed: {str(e)}',
                'config_id': str(config.id),
                'config_name': config.name
            }, status=500)


# ============================================================================
# Scraped Article ViewSet
# ============================================================================

class ScrapedArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing scraped articles.
    Review and approve articles for AI generation.
    """
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'source_config']
    search_fields = ['title', 'content', 'matched_keywords']
    ordering = ['-scraped_at']
    
    def get_queryset(self):
        return ScrapedArticle.objects.select_related(
            'source_config', 'reviewed_by', 'ai_article'
        ).all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ScrapedArticleListSerializer
        return ScrapedArticleSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve scraped article and send to AI generation pipeline.
        
        POST /api/scraped-articles/{id}/approve/
        Body: {"auto_generate": true}
        """
        try:
            article = self.get_object()
            
            if article.status == ScrapedArticle.Status.APPROVED:
                return Response(
                    {'detail': 'Article is already approved.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            article.approve(request.user)
            
            # Optionally auto-queue for generation
            auto_generate = request.data.get('auto_generate', True)
            if auto_generate:
                # Ensure category is lowercase
                category = article.category.lower() if article.category else 'politics'
                
                # Create keyword source from this article
                keyword, created = KeywordSource.objects.get_or_create(
                    keyword=article.title[:255],
                    defaults={
                        'source': 'scraper',
                        'category': category,
                        'status': KeywordSource.Status.APPROVED,
                        'approved_by': request.user,
                        'approved_at': timezone.now(),
                        'notes': f'From scraped article: {article.source_url}'
                    }
                )
                
                # Create AI article for generation
                ai_article = AIArticle.objects.create(
                    keyword=keyword,
                    status=AIArticle.Status.QUEUED,
                    template_type=AIArticle.TemplateType.BREAKING_NEWS
                )
                
                article.ai_article = ai_article
                article.status = ScrapedArticle.Status.GENERATED
                article.save(update_fields=['ai_article', 'status'])
                
                logger.info(f"Article approved and queued: {article.title[:50]}... -> AI Article {ai_article.id}")
                
                return Response({
                    'detail': 'Article approved and generation queued.',
                    'ai_article_id': str(ai_article.id),
                    'scraped_article_id': str(article.id)
                })
            
            return Response({'detail': 'Article approved successfully.'})
            
        except Exception as e:
            logger.error(f"Error approving article {pk}: {str(e)}", exc_info=True)
            return Response(
                {'detail': f'Failed to approve article: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a scraped article.
        
        POST /api/scraped-articles/{id}/reject/
        Body: {"reason": "Not relevant"}
        """
        article = self.get_object()
        reason = request.data.get('reason', '')
        
        if not reason:
            return Response(
                {'detail': 'Rejection reason is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        article.reject(request.user, reason)
        
        return Response({'detail': 'Article rejected.'})
    
    @action(detail=False, methods=['post'])
    def bulk_approve(self, request):
        """
        Bulk approve multiple articles.
        
        POST /api/scraped-articles/bulk_approve/
        Body: {"article_ids": ["uuid1", "uuid2"], "auto_generate": true}
        """
        try:
            article_ids = request.data.get('article_ids', [])
            auto_generate = request.data.get('auto_generate', True)
            
            if not article_ids:
                return Response(
                    {'detail': 'No article IDs provided.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            articles = ScrapedArticle.objects.filter(
                id__in=article_ids,
                status=ScrapedArticle.Status.PENDING
            )
            
            approved_count = 0
            ai_article_ids = []
            errors = []
            
            for article in articles:
                try:
                    article.approve(request.user)
                    approved_count += 1
                    
                    if auto_generate:
                        # Ensure category is lowercase
                        category = article.category.lower() if article.category else 'politics'
                        
                        keyword, created = KeywordSource.objects.get_or_create(
                            keyword=article.title[:255],
                            defaults={
                                'source': 'scraper',
                                'category': category,
                                'status': KeywordSource.Status.APPROVED,
                                'approved_by': request.user,
                                'approved_at': timezone.now()
                            }
                        )
                        
                        ai_article = AIArticle.objects.create(
                            keyword=keyword,
                            status=AIArticle.Status.QUEUED,
                            template_type=AIArticle.TemplateType.BREAKING_NEWS
                        )
                        
                        article.ai_article = ai_article
                        article.status = ScrapedArticle.Status.GENERATED
                        article.save()
                        
                        ai_article_ids.append(str(ai_article.id))
                        
                except Exception as e:
                    logger.error(f"Error approving article {article.id}: {str(e)}")
                    errors.append(f"Article '{article.title[:50]}...': {str(e)}")
                    continue
            
            response_data = {
                'detail': f'Approved {approved_count} articles.',
                'approved_count': approved_count,
                'ai_article_ids': ai_article_ids if auto_generate else []
            }
            
            if errors:
                response_data['errors'] = errors
                
            return Response(response_data)
            
        except Exception as e:
            logger.error(f"Bulk approve error: {str(e)}", exc_info=True)
            return Response(
                {'detail': f'Failed to approve articles: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )