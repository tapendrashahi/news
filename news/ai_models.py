"""
AI Content Generation Models

Task 1.1: Database Models Implementation
- KeywordSource model
- AIArticle model
- AIGenerationConfig model
- AIWorkflowLog model
"""

import uuid
import json
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

User = get_user_model()


# ============================================================================
# Keyword Source Model
# ============================================================================

class KeywordSource(models.Model):
    """
    Keywords/topics for AI article generation.
    Can be manually added or scraped from trending sources.
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
    
    class Source(models.TextChoices):
        MANUAL = 'manual', 'Manual Entry'
        GOOGLE_TRENDS = 'google_trends', 'Google Trends'
        NEWS_API = 'news_api', 'News API'
        TWITTER_TRENDS = 'twitter_trends', 'Twitter Trends'
        INTERNAL = 'internal', 'Internal Analytics'
    
    # Primary Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keyword = models.CharField(max_length=255, unique=True, db_index=True)
    source = models.CharField(max_length=50, choices=Source.choices, default=Source.MANUAL)
    
    # Metrics
    search_volume = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)],
        help_text="Monthly search volume"
    )
    competition = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    viability_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="AI-calculated viability score (0-100)"
    )
    
    # Status & Priority
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    priority = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Priority level (1=highest, 5=lowest)"
    )
    
    # Categorization
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('political', 'Political'),
        ('tech', 'Tech'),
        ('education', 'Education'),
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='business',
        blank=True
    )
    
    # AI Analysis Results
    suggested_angles = models.JSONField(
        default=list, blank=True,
        help_text="AI-suggested article angles"
    )
    related_keywords = models.JSONField(
        default=list, blank=True,
        help_text="Related keywords for SEO"
    )
    suggested_template = models.CharField(
        max_length=50, blank=True,
        help_text="Recommended article template"
    )
    
    # Additional Info
    notes = models.TextField(blank=True)
    
    # Approval
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_keywords'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Keyword Source'
        verbose_name_plural = 'Keyword Sources'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
            models.Index(fields=['category', 'status']),
        ]
    
    def __str__(self):
        return f"{self.keyword} ({self.get_status_display()})"
    
    def approve(self, user):
        """Approve this keyword."""
        self.status = self.Status.APPROVED
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])
    
    def reject(self, user, reason):
        """Reject this keyword."""
        self.status = self.Status.REJECTED
        self.approved_by = user
        self.approved_at = timezone.now()
        self.rejected_reason = reason
        self.save(update_fields=['status', 'approved_by', 'approved_at', 'rejected_reason', 'updated_at'])


# ============================================================================
# AI Article Model
# ============================================================================

class AIArticle(models.Model):
    """
    AI-generated news articles with quality control and workflow tracking.
    """
    
    class Status(models.TextChoices):
        QUEUED = 'queued', 'Queued'
        GENERATING = 'generating', 'Generating'
        REVIEWING = 'reviewing', 'Under Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        PUBLISHED = 'published', 'Published'
        FAILED = 'failed', 'Failed'
    
    class WorkflowStage(models.TextChoices):
        KEYWORD_ANALYSIS = 'keyword_analysis', 'Keyword Analysis'
        RESEARCH = 'research', 'Research & Data Collection'
        OUTLINE = 'outline', 'Outline Generation'
        CONTENT_GENERATION = 'content_generation', 'Content Generation'
        HUMANIZATION = 'humanization', 'Humanization'
        AI_DETECTION = 'ai_detection', 'AI Detection Check'
        PLAGIARISM_CHECK = 'plagiarism_check', 'Plagiarism Check'
        BIAS_DETECTION = 'bias_detection', 'Bias Detection'
        FACT_VERIFICATION = 'fact_verification', 'Fact Verification'
        PERSPECTIVE_ANALYSIS = 'perspective_analysis', 'Perspective Analysis'
        SEO_OPTIMIZATION = 'seo_optimization', 'SEO Optimization'
        META_GENERATION = 'meta_generation', 'Meta Tags Generation'
        IMAGE_GENERATION = 'image_generation', 'Image Generation'
        QUALITY_CHECK = 'quality_check', 'Final Quality Check'
        COMPLETED = 'completed', 'Completed'
    
    class TemplateType(models.TextChoices):
        BREAKING_NEWS = 'breaking_news', 'Breaking News'
        ANALYSIS = 'analysis', 'Analysis & Opinion'
        INVESTIGATIVE = 'investigative', 'Investigative Report'
        FEATURE = 'feature', 'Feature Story'
        DATA_DRIVEN = 'data_driven', 'Data-Driven Report'
        EXPLAINER = 'explainer', 'Explainer'
        LISTICLE = 'listicle', 'Listicle'
    
    # Primary Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keyword = models.ForeignKey(
        KeywordSource,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    published_article = models.OneToOneField(
        'News',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ai_source'
    )
    
    # Article Content
    title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    template_type = models.CharField(
        max_length=50,
        choices=TemplateType.choices,
        default=TemplateType.ANALYSIS
    )
    
    # Status & Workflow
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.QUEUED,
        db_index=True
    )
    workflow_stage = models.CharField(
        max_length=50,
        choices=WorkflowStage.choices,
        default=WorkflowStage.KEYWORD_ANALYSIS,
        db_index=True
    )
    
    # AI Configuration
    ai_model_used = models.CharField(
        max_length=100,
        default='gemini-2.0-flash-exp',
        help_text="AI model used for generation"
    )
    
    # Content Storage (JSON for structured data)
    content_json = models.JSONField(
        default=dict, blank=True,
        help_text="Structured content with sections, headings, etc."
    )
    raw_content = models.TextField(
        blank=True,
        help_text="Raw markdown/HTML content"
    )
    research_data = models.JSONField(
        default=dict, blank=True,
        help_text="Research sources and data collected"
    )
    outline = models.JSONField(
        default=dict, blank=True,
        help_text="Article outline and structure"
    )
    
    # SEO & Meta
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    focus_keywords = models.JSONField(default=list, blank=True)
    og_title = models.CharField(max_length=60, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    
    # Word Count
    target_word_count = models.IntegerField(
        default=1500,
        validators=[MinValueValidator(300), MaxValueValidator(5000)]
    )
    actual_word_count = models.IntegerField(default=0)
    
    # Quality Scores (0-100 scale)
    ai_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="AI detection score (lower is better, <50 target)"
    )
    plagiarism_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Plagiarism percentage (lower is better, <5% target)"
    )
    seo_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="SEO score (higher is better, >75 target)"
    )
    readability_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Readability score (60-80 target)"
    )
    bias_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Bias detection score (lower is better, <20% target - AI Analitica standard)"
    )
    fact_check_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Fact verification score (higher is better, 100% citations required)"
    )
    overall_quality_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Weighted overall quality score"
    )
    
    # Media
    image_url = models.URLField(blank=True, help_text="DALL-E generated image URL")
    image_local_path = models.CharField(max_length=500, blank=True)
    image_prompt = models.TextField(blank=True)
    image_alt_text = models.CharField(max_length=255, blank=True)
    
    # References & Links
    references = models.JSONField(
        default=list, blank=True,
        help_text="List of source references"
    )
    internal_links = models.JSONField(default=list, blank=True)
    external_links = models.JSONField(default=list, blank=True)
    
    # Error Handling
    error_log = models.JSONField(default=list, blank=True)
    retry_count = models.IntegerField(default=0)
    last_error = models.TextField(blank=True)
    failed_stage = models.CharField(max_length=50, blank=True)
    
    # Performance Metrics
    generation_time = models.IntegerField(
        null=True, blank=True,
        help_text="Total generation time in seconds"
    )
    cost_estimate = models.DecimalField(
        max_digits=10, decimal_places=4,
        default=Decimal('0.0000'),
        help_text="Estimated API cost in USD"
    )
    token_usage = models.JSONField(
        default=dict, blank=True,
        help_text="Token usage breakdown by stage"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    generation_started_at = models.DateTimeField(null=True, blank=True)
    generation_completed_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Review
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reviewed_ai_articles'
    )
    review_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Article'
        verbose_name_plural = 'AI Articles'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['workflow_stage', 'status']),
            models.Index(fields=['keyword', 'status']),
        ]
    
    def __str__(self):
        return self.title or f"AI Article for: {self.keyword.keyword}"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from title."""
        if self.title and not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while AIArticle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def is_ready_for_review(self):
        """Check if article is ready for human review."""
        return (
            self.status == self.Status.REVIEWING and
            self.workflow_stage == self.WorkflowStage.COMPLETED
        )
    
    @property
    def passes_quality_threshold(self):
        """Check if article meets all quality thresholds."""
        checks = [
            self.ai_score is None or self.ai_score < 50,  # AI detection
            self.plagiarism_score is None or self.plagiarism_score < 5,  # Plagiarism
            self.seo_score is None or self.seo_score >= 75,  # SEO
            self.readability_score is None or self.readability_score >= 60,  # Readability
            self.bias_score is None or self.bias_score < 20,  # Bias (AI Analitica)
            self.fact_check_score is None or self.fact_check_score >= 80,  # Facts
        ]
        return all(checks)
    
    def calculate_overall_quality(self):
        """Calculate weighted overall quality score."""
        weights = {
            'bias': 0.25,  # Highest weight for AI Analitica mission
            'fact_check': 0.25,
            'seo': 0.15,
            'readability': 0.15,
            'ai_detection': 0.10,  # Inverted (lower is better)
            'plagiarism': 0.10,  # Inverted (lower is better)
        }
        
        scores = {}
        if self.bias_score is not None:
            scores['bias'] = 100 - float(self.bias_score)  # Invert
        if self.fact_check_score is not None:
            scores['fact_check'] = float(self.fact_check_score)
        if self.seo_score is not None:
            scores['seo'] = float(self.seo_score)
        if self.readability_score is not None:
            scores['readability'] = float(self.readability_score)
        if self.ai_score is not None:
            scores['ai_detection'] = 100 - float(self.ai_score)  # Invert
        if self.plagiarism_score is not None:
            scores['plagiarism'] = 100 - float(self.plagiarism_score)  # Invert
        
        if not scores:
            return None
        
        total_weight = sum(weights[k] for k in scores.keys())
        weighted_sum = sum(scores[k] * weights[k] for k in scores.keys())
        
        return Decimal(str(round(weighted_sum / total_weight, 2)))
    
    def get_next_stage(self):
        """Determine the next workflow stage."""
        stages = list(self.WorkflowStage.values)
        try:
            current_index = stages.index(self.workflow_stage)
            if current_index < len(stages) - 1:
                return stages[current_index + 1]
        except ValueError:
            pass
        return self.WorkflowStage.COMPLETED
    
    def advance_stage(self):
        """Move to the next workflow stage."""
        self.workflow_stage = self.get_next_stage()
        if self.workflow_stage == self.WorkflowStage.COMPLETED:
            self.status = self.Status.REVIEWING
            self.generation_completed_at = timezone.now()
        self.save(update_fields=['workflow_stage', 'status', 'generation_completed_at', 'updated_at'])
    
    def log_error(self, stage, error_message):
        """Log an error during generation."""
        error_entry = {
            'timestamp': timezone.now().isoformat(),
            'stage': stage,
            'error': error_message,
            'retry_count': self.retry_count
        }
        if not isinstance(self.error_log, list):
            self.error_log = []
        self.error_log.append(error_entry)
        self.last_error = error_message
        self.failed_stage = stage
        self.save(update_fields=['error_log', 'last_error', 'failed_stage', 'updated_at'])


# ============================================================================
# AI Generation Config Model
# ============================================================================

class AIGenerationConfig(models.Model):
    """
    Configuration templates for AI article generation.
    Defines prompts, parameters, and quality thresholds.
    """
    
    class Provider(models.TextChoices):
        OPENAI = 'openai', 'OpenAI'
        ANTHROPIC = 'anthropic', 'Anthropic (Claude)'
        GOOGLE = 'google', 'Google (Gemini)'
        GROQ = 'groq', 'Groq (Ultra-Fast)'
        NATURALWRITE = 'naturalwrite', 'NaturalWrite (Humanizer)'
        HUGGINGFACE = 'huggingface', 'Hugging Face (Models)'
    
    # Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    template_type = models.CharField(
        max_length=50,
        choices=AIArticle.TemplateType.choices,
        default=AIArticle.TemplateType.ANALYSIS
    )
    
    # AI Provider Settings
    ai_provider = models.CharField(
        max_length=50,
        choices=Provider.choices,
        default=Provider.GOOGLE
    )
    model_name = models.CharField(
        max_length=100,
        default='gemini-2.0-flash-exp',
        help_text="Model name (e.g., gemini-2.0-flash-exp, gpt-4, claude-3-opus)"
    )
    
    # Prompts
    system_prompt = models.TextField(
        help_text="System prompt defining AI behavior and mission (AI Analitica standards)"
    )
    user_prompt_template = models.TextField(
        help_text="User prompt template with placeholders: {keyword}, {word_count}, etc."
    )
    outline_prompt = models.TextField(blank=True)
    research_prompt = models.TextField(blank=True)
    
    # Model Parameters
    temperature = models.DecimalField(
        max_digits=3, decimal_places=2,
        default=Decimal('0.7'),
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )
    max_tokens = models.IntegerField(
        default=8000,
        validators=[MinValueValidator(100), MaxValueValidator(128000)]
    )
    top_p = models.DecimalField(
        max_digits=3, decimal_places=2,
        default=Decimal('1.0'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    frequency_penalty = models.DecimalField(
        max_digits=3, decimal_places=2,
        default=Decimal('0.0'),
        validators=[MinValueValidator(-2), MaxValueValidator(2)]
    )
    presence_penalty = models.DecimalField(
        max_digits=3, decimal_places=2,
        default=Decimal('0.0'),
        validators=[MinValueValidator(-2), MaxValueValidator(2)]
    )
    
    # Content Settings
    target_word_count = models.IntegerField(
        default=1500,
        validators=[MinValueValidator(300), MaxValueValidator(5000)]
    )
    num_headings = models.IntegerField(
        default=5,
        validators=[MinValueValidator(2), MaxValueValidator(15)]
    )
    include_statistics = models.BooleanField(default=True)
    include_quotes = models.BooleanField(default=True)
    include_internal_links = models.BooleanField(default=True)
    
    # Quality Thresholds
    max_ai_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=Decimal('50.00'),
        help_text="Maximum acceptable AI detection score"
    )
    max_plagiarism_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=Decimal('5.00'),
        help_text="Maximum acceptable plagiarism percentage"
    )
    min_seo_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=Decimal('75.00'),
        help_text="Minimum acceptable SEO score"
    )
    min_readability_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=Decimal('60.00'),
        help_text="Minimum acceptable readability score"
    )
    max_bias_score = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=Decimal('20.00'),
        help_text="Maximum acceptable bias score (AI Analitica: <20%)"
    )
    
    # Automation Settings
    auto_humanize = models.BooleanField(
        default=True,
        help_text="Automatically humanize AI-generated content"
    )
    auto_rewrite_plagiarism = models.BooleanField(
        default=True,
        help_text="Automatically rewrite plagiarized sections"
    )
    auto_publish = models.BooleanField(
        default=False,
        help_text="Automatically publish if all quality checks pass"
    )
    max_retries = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    
    # Per-Stage AI Configuration (JSON field storing provider/model for each stage)
    stage_configs = models.JSONField(
        default=dict,
        blank=True,
        help_text="Per-stage AI provider and model configuration. Format: {'outline': {'provider': 'groq', 'model': 'llama-3.1-8b-instant'}, ...}"
    )
    
    # Status
    enabled = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    
    # Timestamps & User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ai_configs'
    )
    
    class Meta:
        ordering = ['-is_default', 'name']
        verbose_name = 'AI Generation Config'
        verbose_name_plural = 'AI Generation Configs'
    
    def __str__(self):
        default_str = " (Default)" if self.is_default else ""
        return f"{self.name}{default_str}"
    
    def save(self, *args, **kwargs):
        """Ensure only one default config per template type."""
        if self.is_default:
            AIGenerationConfig.objects.filter(
                template_type=self.template_type,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


# ============================================================================
# AI Workflow Log Model
# ============================================================================

class AIWorkflowLog(models.Model):
    """
    Detailed logs of each workflow stage execution.
    Tracks performance, errors, and AI responses.
    """
    
    class LogStatus(models.TextChoices):
        STARTED = 'started', 'Started'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        SKIPPED = 'skipped', 'Skipped'
    
    # Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(
        AIArticle,
        on_delete=models.CASCADE,
        related_name='workflow_logs'
    )
    
    # Stage Info
    stage = models.CharField(
        max_length=50,
        choices=AIArticle.WorkflowStage.choices
    )
    status = models.CharField(
        max_length=20,
        choices=LogStatus.choices,
        default=LogStatus.STARTED
    )
    
    # Data
    input_data = models.JSONField(
        default=dict, blank=True,
        help_text="Input data for this stage"
    )
    output_data = models.JSONField(
        default=dict, blank=True,
        help_text="Output/result from this stage"
    )
    
    # Error Info
    error_message = models.TextField(blank=True)
    error_traceback = models.TextField(blank=True)
    
    # Performance Metrics
    execution_time = models.IntegerField(
        default=0,
        help_text="Execution time in milliseconds"
    )
    tokens_used = models.IntegerField(default=0)
    cost = models.DecimalField(
        max_digits=10, decimal_places=4,
        default=Decimal('0.0000')
    )
    ai_model = models.CharField(max_length=100, blank=True)
    
    # Retry Info
    retry_number = models.IntegerField(default=0)
    triggered_by = models.CharField(
        max_length=50,
        choices=[('auto', 'Automatic'), ('manual', 'Manual Retry')],
        default='auto'
    )
    
    # Timestamps
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'AI Workflow Log'
        verbose_name_plural = 'AI Workflow Logs'
        indexes = [
            models.Index(fields=['article', 'stage']),
            models.Index(fields=['status', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.article.title or 'Article'} - {self.get_stage_display()} ({self.get_status_display()})"
    
    def mark_completed(self, output_data=None):
        """Mark this log entry as completed."""
        self.status = self.LogStatus.COMPLETED
        self.completed_at = timezone.now()
        if output_data:
            self.output_data = output_data
        self.save(update_fields=['status', 'completed_at', 'output_data'])
    
    def mark_failed(self, error_message, error_traceback=None):
        """Mark this log entry as failed."""
        self.status = self.LogStatus.FAILED
        self.error_message = error_message
        self.error_traceback = error_traceback or ''
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'error_traceback', 'completed_at'])


# ============================================================================
# News Source Configuration Model
# ============================================================================

class NewsSourceConfig(models.Model):
    """
    Configuration for news scraping sources.
    Defines keywords and target websites for content discovery.
    """
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
        DISABLED = 'disabled', 'Disabled'
    
    # Primary Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Configuration name")
    
    # Keywords to search for
    keywords = models.JSONField(
        default=list,
        help_text="List of keywords/topics to search for"
    )
    
    # Target websites
    source_websites = models.JSONField(
        default=list,
        help_text="List of news website URLs to scrape from"
    )
    
    # Category
    CATEGORY_CHOICES = [
        ('Politics', 'Politics'),
        ('Business', 'Business'),
        ('Technology', 'Technology'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Sports', 'Sports'),
        ('Science', 'Science'),
        ('Environment', 'Environment'),
        ('Culture', 'Culture'),
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Politics'
    )
    
    # Settings
    max_articles_per_scrape = models.IntegerField(
        default=20,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    scrape_frequency_hours = models.IntegerField(
        default=24,
        help_text="How often to scrape (in hours)"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    
    # Metadata
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_source_configs'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_scraped_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News Source Configuration'
        verbose_name_plural = 'News Source Configurations'
    
    def __str__(self):
        return f"{self.name} - {self.category}"


# ============================================================================
# Scraped Article Model
# ============================================================================

class ScrapedArticle(models.Model):
    """
    Articles scraped from news websites.
    Pending review before sending to AI generation pipeline.
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        APPROVED = 'approved', 'Approved for Generation'
        REJECTED = 'rejected', 'Rejected'
        GENERATED = 'generated', 'Article Generated'
    
    # Primary Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_config = models.ForeignKey(
        NewsSourceConfig,
        on_delete=models.CASCADE,
        related_name='scraped_articles'
    )
    
    # Article Data
    title = models.CharField(max_length=500)
    content = models.TextField(help_text="Scraped article content")
    summary = models.TextField(blank=True)
    
    # Source Information
    source_url = models.URLField(max_length=1000)
    source_website = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    
    # Extracted Data
    matched_keywords = models.JSONField(
        default=list,
        help_text="Keywords that matched this article"
    )
    image_urls = models.JSONField(
        default=list,
        help_text="Image URLs found in article"
    )
    reference_urls = models.JSONField(
        default=list,
        help_text="Reference/citation URLs from article"
    )
    
    # Categorization
    category = models.CharField(max_length=50)
    tags = models.JSONField(default=list, blank=True)
    
    # Review Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    
    # Approval/Rejection
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reviewed_scraped_articles'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Link to generated AI article
    ai_article = models.ForeignKey(
        AIArticle,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='source_scraped_article'
    )
    
    # Timestamps
    scraped_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scraped_at']
        verbose_name = 'Scraped Article'
        verbose_name_plural = 'Scraped Articles'
        indexes = [
            models.Index(fields=['status', '-scraped_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['source_config', '-scraped_at']),
        ]
    
    def __str__(self):
        return f"{self.title[:50]}... ({self.get_status_display()})"
    
    def approve(self, user):
        """Approve this article for AI generation."""
        self.status = self.Status.APPROVED
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'updated_at'])
    
    def reject(self, user, reason):
        """Reject this article."""
        self.status = self.Status.REJECTED
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.rejection_reason = reason
        self.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'rejection_reason', 'updated_at'])

