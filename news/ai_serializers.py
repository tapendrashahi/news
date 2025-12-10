"""
AI Content API Serializers

Task 1.2: API Serializers Implementation
- KeywordSourceSerializer
- KeywordSourceListSerializer
- AIArticleSerializer
- AIArticleListSerializer
- AIArticleDetailSerializer
- AIGenerationConfigSerializer
- AIWorkflowLogSerializer
"""


"""
AI-Generated News Automation System - API Serializers
======================================================
Serializers for the AI news generation pipeline API.

Includes full and lightweight versions for different use cases:
- Full serializers: Complete data with nested relationships
- List serializers: Lightweight for list views and queues
- Detail serializers: Extended data with workflow logs
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .ai_models import (
    KeywordSource, AIArticle, AIGenerationConfig, AIWorkflowLog,
    NewsSourceConfig, ScrapedArticle
)
from .models import News

User = get_user_model()


# ============================================================================
# User Serializers (for nested relationships)
# ============================================================================

class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user data for nested relationships."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


# ============================================================================
# Published Article Serializer (for nested relationships)
# ============================================================================

class PublishedArticleSerializer(serializers.ModelSerializer):
    """Minimal serializer for published News articles."""
    class Meta:
        model = News
        fields = ['id', 'title', 'slug', 'publish_date']
        read_only_fields = ['id', 'title', 'slug', 'publish_date']

class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user data for nested relationships."""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']
        read_only_fields = fields
    
    def get_full_name(self, obj):
        return obj.get_full_name() if hasattr(obj, 'get_full_name') else obj.username


# ============================================================================
# Keyword Source Serializers
# ============================================================================

class KeywordSourceSerializer(serializers.ModelSerializer):
    """Full serializer for KeywordSource with all fields."""
    
    approved_by = UserMinimalSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    articles_count = serializers.SerializerMethodField()
    can_generate = serializers.SerializerMethodField()
    
    class Meta:
        model = KeywordSource
        fields = [
            'id', 'keyword', 'source', 'search_volume', 'competition',
            'status', 'priority', 'category', 'category_display', 'notes',
            'viability_score', 'suggested_angles', 'related_keywords',
            'suggested_template', 'created_at', 'updated_at',
            'approved_by', 'approved_at', 'rejected_reason',
            'articles_count', 'can_generate'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'approved_by', 'approved_at',
            'viability_score', 'suggested_angles', 'related_keywords',
            'suggested_template', 'articles_count', 'can_generate'
        ]
    
    def get_articles_count(self, obj):
        return obj.articles.count()
    
    def get_can_generate(self, obj):
        """Check if this keyword can be used for article generation."""
        return obj.status == KeywordSource.Status.APPROVED


class KeywordSourceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    has_articles = serializers.SerializerMethodField()
    
    class Meta:
        model = KeywordSource
        fields = [
            'id', 'keyword', 'source', 'search_volume', 'competition',
            'status', 'priority', 'category', 'category_display',
            'viability_score', 'created_at', 'approved_by_name',
            'approved_at', 'has_articles'
        ]
        read_only_fields = fields
    
    def get_has_articles(self, obj):
        return obj.articles.exists()


class KeywordSourceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new keywords."""
    
    class Meta:
        model = KeywordSource
        fields = [
            'keyword', 'source', 'search_volume', 'competition',
            'priority', 'category', 'notes'
        ]
    
    def validate_keyword(self, value):
        """Ensure keyword is not a duplicate."""
        if KeywordSource.objects.filter(keyword__iexact=value).exists():
            raise serializers.ValidationError("This keyword already exists.")
        return value


class KeywordApprovalSerializer(serializers.Serializer):
    """Serializer for keyword approval/rejection."""
    
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    reason = serializers.CharField(required=False, allow_blank=True, max_length=500)
    
    def validate(self, data):
        if data['action'] == 'reject' and not data.get('reason'):
            raise serializers.ValidationError({
                'reason': 'Rejection reason is required when rejecting a keyword.'
            })
        return data


class KeywordBulkActionSerializer(serializers.Serializer):
    """Serializer for bulk keyword actions."""
    
    keyword_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        max_length=100
    )
    action = serializers.ChoiceField(
        choices=['approve', 'reject', 'delete', 'set_priority']
    )
    reason = serializers.CharField(required=False, allow_blank=True)
    priority = serializers.IntegerField(required=False, min_value=1, max_value=5)
    
    def validate(self, data):
        if data['action'] == 'set_priority' and 'priority' not in data:
            raise serializers.ValidationError({
                'priority': 'Priority is required for set_priority action.'
            })
        return data


# ============================================================================
# AI Article Serializers
# ============================================================================

class AIArticleSerializer(serializers.ModelSerializer):
    """Full serializer for AIArticle with nested data."""
    
    keyword_data = KeywordSourceListSerializer(source='keyword', read_only=True)
    reviewed_by = UserMinimalSerializer(read_only=True)
    published_article = PublishedArticleSerializer(read_only=True)
    category_display = serializers.CharField(source='keyword.get_category_display', read_only=True)
    workflow_progress = serializers.SerializerMethodField()
    quality_summary = serializers.SerializerMethodField()
    is_ready_for_review = serializers.BooleanField(read_only=True)
    passes_quality_threshold = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = AIArticle
        fields = [
            'id', 'keyword', 'keyword_data', 'published_article',
            'title', 'slug', 'template_type', 'status', 'workflow_stage',
            'ai_model_used', 'content_json', 'raw_content', 'research_data',
            'outline', 'meta_title', 'meta_description', 'focus_keywords',
            'og_title', 'og_description', 'target_word_count', 'actual_word_count',
            'ai_score', 'plagiarism_score', 'seo_score', 'readability_score',
            'bias_score', 'fact_check_score', 'overall_quality_score',
            'image_url', 'image_local_path', 'image_prompt', 'image_alt_text',
            'references', 'internal_links', 'external_links',
            'error_log', 'retry_count', 'last_error', 'failed_stage',
            'generation_time', 'cost_estimate', 'token_usage',
            'created_at', 'updated_at', 'generation_started_at',
            'generation_completed_at', 'published_at',
            'reviewed_by', 'review_notes', 'category_display',
            'workflow_progress', 'quality_summary',
            'is_ready_for_review', 'passes_quality_threshold'
        ]
        read_only_fields = [
            'id', 'slug', 'content_json', 'raw_content', 'research_data',
            'outline', 'actual_word_count', 'ai_score', 'plagiarism_score',
            'seo_score', 'readability_score', 'bias_score', 'fact_check_score',
            'overall_quality_score', 'image_url', 'image_local_path',
            'image_prompt', 'image_alt_text', 'references', 'internal_links',
            'external_links', 'error_log', 'retry_count', 'last_error',
            'failed_stage', 'generation_time', 'cost_estimate', 'token_usage',
            'created_at', 'updated_at', 'generation_started_at',
            'generation_completed_at', 'published_at', 'reviewed_by',
            'workflow_progress', 'quality_summary', 'is_ready_for_review',
            'passes_quality_threshold'
        ]
    
    def get_workflow_progress(self, obj):
        """Calculate workflow progress percentage."""
        stages = list(AIArticle.WorkflowStage.values)
        current_index = stages.index(obj.workflow_stage) if obj.workflow_stage in stages else 0
        total_stages = len(stages)
        return {
            'current_stage': obj.workflow_stage,
            'current_stage_display': obj.get_workflow_stage_display(),
            'current_index': current_index,
            'total_stages': total_stages,
            'percentage': round((current_index / total_stages) * 100, 1)
        }
    
    def get_quality_summary(self, obj):
        """Get a summary of quality scores with pass/fail status."""
        return {
            'ai_detection': {
                'score': obj.ai_score,
                'threshold': 50,
                'passed': obj.ai_score is None or obj.ai_score < 50
            },
            'plagiarism': {
                'score': obj.plagiarism_score,
                'threshold': 5,
                'passed': obj.plagiarism_score is None or obj.plagiarism_score < 5
            },
            'seo': {
                'score': obj.seo_score,
                'threshold': 75,
                'passed': obj.seo_score is None or obj.seo_score >= 75
            },
            'readability': {
                'score': obj.readability_score,
                'threshold': 60,
                'passed': obj.readability_score is None or obj.readability_score >= 60
            },
            'bias': {
                'score': obj.bias_score,
                'threshold': 20,
                'passed': obj.bias_score is None or obj.bias_score < 20
            },
            'fact_check': {
                'score': obj.fact_check_score,
                'threshold': 80,
                'passed': obj.fact_check_score is None or obj.fact_check_score >= 80
            },
            'overall': obj.overall_quality_score,
            'all_passed': obj.passes_quality_threshold
        }


class AIArticleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for queue views and list displays."""
    
    keyword_text = serializers.CharField(source='keyword.keyword', read_only=True)
    category_display = serializers.CharField(source='keyword.get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    workflow_stage_display = serializers.CharField(source='get_workflow_stage_display', read_only=True)
    published_article = PublishedArticleSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    has_errors = serializers.SerializerMethodField()
    
    class Meta:
        model = AIArticle
        fields = [
            'id', 'title', 'slug', 'keyword_text', 'category_display',
            'template_type', 'status', 'status_display',
            'workflow_stage', 'workflow_stage_display',
            'ai_model_used', 'actual_word_count',
            'overall_quality_score', 'cost_estimate',
            'created_at', 'updated_at', 'progress_percentage',
            'has_errors', 'retry_count', 'published_article',
            # Content fields for Review Queue
            'raw_content', 'content_json', 'meta_title', 
            'meta_description', 'focus_keywords',
            'ai_score', 'plagiarism_score', 'seo_score', 
            'readability_score', 'bias_score', 'fact_check_score',
            'research_data', 'outline'
        ]
        read_only_fields = fields
    
    def get_progress_percentage(self, obj):
        stages = list(AIArticle.WorkflowStage.values)
        current_index = stages.index(obj.workflow_stage) if obj.workflow_stage in stages else 0
        return round((current_index / len(stages)) * 100, 1)
    
    def get_has_errors(self, obj):
        return bool(obj.last_error) or len(obj.error_log) > 0


class AIArticleDetailSerializer(AIArticleSerializer):
    """Extended serializer that includes workflow logs."""
    
    workflow_logs = serializers.SerializerMethodField()
    latest_logs = serializers.SerializerMethodField()
    
    class Meta(AIArticleSerializer.Meta):
        fields = AIArticleSerializer.Meta.fields + ['workflow_logs', 'latest_logs']
    
    def get_workflow_logs(self, obj):
        """Get all workflow logs for this article."""
        logs = obj.workflow_logs.all().order_by('timestamp')
        return AIWorkflowLogSerializer(logs, many=True).data
    
    def get_latest_logs(self, obj):
        """Get the 5 most recent workflow logs."""
        logs = obj.workflow_logs.all().order_by('-timestamp')[:5]
        return AIWorkflowLogSerializer(logs, many=True).data


class AIArticleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new AI articles."""
    
    class Meta:
        model = AIArticle
        fields = [
            'keyword', 'template_type', 'ai_model_used',
            'target_word_count', 'meta_title', 'meta_description'
        ]
    
    def validate_keyword(self, value):
        """Ensure keyword is approved and not already processed."""
        if value.status != KeywordSource.Status.APPROVED:
            raise serializers.ValidationError(
                "Only approved keywords can be used for article generation."
            )
        return value
    
    def create(self, validated_data):
        """Create article and set initial status."""
        validated_data['status'] = AIArticle.Status.QUEUED
        validated_data['workflow_stage'] = AIArticle.WorkflowStage.KEYWORD_ANALYSIS
        return super().create(validated_data)


class AIArticleReviewSerializer(serializers.Serializer):
    """Serializer for article review actions."""
    
    action = serializers.ChoiceField(
        choices=['approve', 'reject', 'request_changes', 'publish']
    )
    notes = serializers.CharField(required=False, allow_blank=True, max_length=2000)
    
    def validate(self, data):
        if data['action'] in ['reject', 'request_changes'] and not data.get('notes'):
            raise serializers.ValidationError({
                'notes': f"Notes are required when {data['action'].replace('_', ' ')}ing an article."
            })
        return data


class AIArticleRetrySerializer(serializers.Serializer):
    """Serializer for retry actions."""
    
    stage = serializers.ChoiceField(
        choices=AIArticle.WorkflowStage.choices,
        required=False,
        help_text="Specific stage to retry from. If not provided, retries from failed stage."
    )
    force = serializers.BooleanField(
        default=False,
        help_text="Force retry even if max retries exceeded."
    )


# ============================================================================
# AI Generation Config Serializers
# ============================================================================

class AIGenerationConfigSerializer(serializers.ModelSerializer):
    """Full serializer for AIGenerationConfig."""
    
    created_by = UserMinimalSerializer(read_only=True)
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AIGenerationConfig
        fields = [
            'id', 'name', 'description', 'template_type',
            'ai_provider', 'model_name', 'system_prompt',
            'user_prompt_template', 'outline_prompt', 'research_prompt',
            'temperature', 'max_tokens', 'top_p',
            'frequency_penalty', 'presence_penalty',
            'target_word_count', 'num_headings',
            'include_statistics', 'include_quotes', 'include_internal_links',
            'max_ai_score', 'max_plagiarism_score', 'min_seo_score',
            'min_readability_score', 'max_bias_score',
            'auto_humanize', 'auto_rewrite_plagiarism', 'auto_publish',
            'max_retries', 'enabled', 'is_default', 'version',
            'stage_configs',
            'created_at', 'updated_at', 'created_by', 'usage_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'usage_count']
    
    def get_usage_count(self, obj):
        """Count how many articles used this config."""
        # This would require tracking config usage in AIArticle
        return 0  # Placeholder
    
    def validate_name(self, value):
        """Ensure config name is unique."""
        instance = self.instance
        if AIGenerationConfig.objects.filter(name__iexact=value).exclude(
            pk=instance.pk if instance else None
        ).exists():
            raise serializers.ValidationError("A config with this name already exists.")
        return value
    
    def validate(self, data):
        """Validate prompt templates have required placeholders."""
        if 'user_prompt_template' in data:
            required_placeholders = ['{keyword}', '{word_count}']
            for placeholder in required_placeholders:
                if placeholder not in data['user_prompt_template']:
                    raise serializers.ValidationError({
                        'user_prompt_template': f"Template must include {placeholder}"
                    })
        return data


class AIGenerationConfigListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for config list views."""
    
    class Meta:
        model = AIGenerationConfig
        fields = [
            'id', 'name', 'template_type', 'ai_provider', 'model_name',
            'enabled', 'is_default', 'version', 'updated_at'
        ]
        read_only_fields = fields


# ============================================================================
# AI Workflow Log Serializers
# ============================================================================

class AIWorkflowLogSerializer(serializers.ModelSerializer):
    """Full serializer for AIWorkflowLog."""
    
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = AIWorkflowLog
        fields = [
            'id', 'article', 'stage', 'stage_display',
            'status', 'status_display', 'input_data', 'output_data',
            'error_message', 'error_traceback', 'execution_time',
            'tokens_used', 'cost', 'ai_model', 'retry_number',
            'triggered_by', 'timestamp', 'completed_at', 'duration_formatted'
        ]
        read_only_fields = fields
    
    def get_duration_formatted(self, obj):
        """Format execution time in human-readable format."""
        ms = obj.execution_time
        if ms < 1000:
            return f"{ms}ms"
        elif ms < 60000:
            return f"{ms / 1000:.1f}s"
        else:
            minutes = ms // 60000
            seconds = (ms % 60000) / 1000
            return f"{minutes}m {seconds:.1f}s"


class AIWorkflowLogListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for log list views."""
    
    stage_display = serializers.CharField(source='get_stage_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AIWorkflowLog
        fields = [
            'id', 'stage', 'stage_display', 'status', 'status_display',
            'execution_time', 'cost', 'timestamp', 'completed_at'
        ]
        read_only_fields = fields


# ============================================================================
# Statistics & Analytics Serializers
# ============================================================================

class AIContentStatsSerializer(serializers.Serializer):
    """Serializer for AI content statistics."""
    
    total_keywords = serializers.IntegerField()
    pending_keywords = serializers.IntegerField()
    approved_keywords = serializers.IntegerField()
    
    total_articles = serializers.IntegerField()
    queued_articles = serializers.IntegerField()
    generating_articles = serializers.IntegerField()
    ready_articles = serializers.IntegerField()
    published_articles = serializers.IntegerField()
    failed_articles = serializers.IntegerField()
    
    average_quality_score = serializers.FloatField()
    average_generation_time = serializers.FloatField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    articles_today = serializers.IntegerField()
    articles_this_week = serializers.IntegerField()
    articles_this_month = serializers.IntegerField()


class AIQueueStatusSerializer(serializers.Serializer):
    """Serializer for real-time queue status."""
    
    queue_length = serializers.IntegerField()
    currently_processing = serializers.IntegerField()
    estimated_wait_time = serializers.IntegerField(help_text="Estimated wait time in minutes")
    
    recent_completions = AIArticleListSerializer(many=True)
    recent_failures = AIArticleListSerializer(many=True)
    currently_generating = AIArticleListSerializer(many=True)


class GenerationProgressSerializer(serializers.Serializer):
    """Serializer for article generation progress updates."""
    
    article_id = serializers.UUIDField()
    title = serializers.CharField()
    current_stage = serializers.CharField()
    current_stage_display = serializers.CharField()
    progress_percentage = serializers.FloatField()
    status = serializers.CharField()
    elapsed_time = serializers.IntegerField(help_text="Elapsed time in seconds")
    estimated_remaining = serializers.IntegerField(
        help_text="Estimated remaining time in seconds",
        allow_null=True
    )
    stages_completed = serializers.ListField(child=serializers.CharField())
    current_stage_message = serializers.CharField(allow_blank=True)


# ============================================================================
# News Source & Scraped Article Serializers
# ============================================================================

class NewsSourceConfigSerializer(serializers.ModelSerializer):
    """Serializer for news source configuration."""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = NewsSourceConfig
        fields = [
            'id', 'name', 'keywords', 'source_websites', 'category',
            'max_articles_per_scrape', 'scrape_frequency_hours', 'status',
            'notes', 'created_by', 'created_by_name', 'created_at', 
            'updated_at', 'last_scraped_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_scraped_at', 'created_by_name']
    
    def create(self, validated_data):
        # Set created_by from request user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ScrapedArticleSerializer(serializers.ModelSerializer):
    """Serializer for scraped articles."""
    source_config_name = serializers.CharField(source='source_config.name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True)
    ai_article_id = serializers.UUIDField(source='ai_article.id', read_only=True)
    
    class Meta:
        model = ScrapedArticle
        fields = [
            'id', 'source_config', 'source_config_name', 'title', 'content', 
            'summary', 'source_url', 'source_website', 'author', 'published_date',
            'matched_keywords', 'image_urls', 'reference_urls', 'category', 'tags',
            'status', 'reviewed_by', 'reviewed_by_name', 'reviewed_at', 
            'rejection_reason', 'ai_article', 'ai_article_id', 'scraped_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'source_config_name', 'reviewed_by', 'reviewed_by_name', 
            'reviewed_at', 'ai_article', 'ai_article_id', 'scraped_at', 'updated_at'
        ]


class ScrapedArticleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for scraped article lists."""
    source_config_name = serializers.CharField(source='source_config.name', read_only=True)
    
    class Meta:
        model = ScrapedArticle
        fields = [
            'id', 'title', 'source_website', 'source_url', 'category',
            'status', 'matched_keywords', 'source_config_name', 'scraped_at'
        ]
        read_only_fields = fields