from django.contrib import admin
from .models import News, TeamMember, Comment, ShareCount, JobOpening, JobApplication, LegalPage
from .ai_models import KeywordSource, AIArticle, AIGenerationConfig, AIWorkflowLog
from django.utils.html import format_html

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'visibility', 'publish_date', 'created_at', 'preview_image')
    list_filter = ('category', 'visibility', 'created_at', 'author')
    search_fields = ('title', 'content', 'slug', 'tags', 'excerpt', 'author__name')
    fields = ('title', 'slug', 'content', 'excerpt', 'category', 'tags', 'author', 'meta_description', 'visibility', 'publish_date', 'image', 'preview_image_display')
    readonly_fields = ('preview_image_display',)
    prepopulated_fields = {'slug': ('title',)}

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    preview_image.short_description = 'Thumbnail'

    def preview_image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No image uploaded"
    preview_image_display.short_description = 'Current Image Preview'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'preview_photo', 'email', 'is_active', 'order', 'joined_date')
    list_filter = ('role', 'is_active', 'joined_date')
    search_fields = ('name', 'role', 'email', 'bio')
    list_editable = ('order', 'is_active')
    fields = (
        'name', 
        'role', 
        'bio', 
        'email',
        'photo',
        'photo_preview',
        'twitter_url', 
        'linkedin_url', 
        'is_active', 
        'order'
    )
    readonly_fields = ('photo_preview', 'joined_date')
    
    def preview_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', 
                obj.photo.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #0f3460, #e94560); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{}</div>',
            obj.name[0] if obj.name else '?'
        )
    preview_photo.short_description = 'Photo'
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="200" height="200" style="object-fit: cover; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', 
                obj.photo.url
            )
        return "No photo uploaded - A placeholder will be shown on the website"
    photo_preview.short_description = 'Current Photo Preview'
    
    # Custom action for bulk activation/deactivation
    actions = ['activate_members', 'deactivate_members']
    
    def activate_members(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} team member(s) activated successfully.')
    activate_members.short_description = "Activate selected team members"
    
    def deactivate_members(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} team member(s) deactivated successfully.')
    deactivate_members.short_description = "Deactivate selected team members"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'news', 'text_preview', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'text', 'news__title')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    fields = ('news', 'name', 'email', 'text', 'is_approved', 'created_at')
    
    def text_preview(self, obj):
        return obj.text[:75] + '...' if len(obj.text) > 75 else obj.text
    text_preview.short_description = 'Comment'
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comment(s) approved successfully.')
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comment(s) unapproved successfully.')
    unapprove_comments.short_description = "Unapprove selected comments"


@admin.register(ShareCount)
class ShareCountAdmin(admin.ModelAdmin):
    list_display = ('news', 'platform', 'count', 'last_shared')
    list_filter = ('platform', 'last_shared')
    search_fields = ('news__title',)
    readonly_fields = ('last_shared',)
    ordering = ('-count',)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'employment_type', 'experience_level', 'is_active', 'posted_date', 'application_count')
    list_filter = ('department', 'employment_type', 'experience_level', 'is_active', 'posted_date')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('posted_date', 'updated_date', 'application_count')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'department', 'location', 'employment_type', 'experience_level')
        }),
        ('Job Details', {
            'fields': ('description', 'responsibilities', 'requirements', 'salary_range')
        }),
        ('Status & Dates', {
            'fields': ('is_active', 'application_deadline', 'posted_date', 'updated_date', 'application_count')
        }),
    )
    
    def application_count(self, obj):
        count = obj.applications.count()
        return format_html('<strong>{}</strong> application(s)', count)
    application_count.short_description = 'Applications'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_opening', 'email', 'phone', 'years_of_experience', 'status', 'applied_date', 'resume_link')
    list_filter = ('status', 'applied_date', 'job_opening__department', 'years_of_experience')
    search_fields = ('full_name', 'email', 'phone', 'job_opening__title')
    readonly_fields = ('applied_date', 'updated_date', 'resume_preview')
    actions = ['mark_under_review', 'mark_interview', 'mark_rejected', 'mark_accepted']
    fieldsets = (
        ('Job & Applicant Info', {
            'fields': ('job_opening', 'full_name', 'email', 'phone', 'years_of_experience')
        }),
        ('Application Materials', {
            'fields': ('resume', 'resume_preview', 'cover_letter', 'linkedin_url', 'portfolio_url')
        }),
        ('Application Status', {
            'fields': ('status', 'notes', 'applied_date', 'updated_date')
        }),
    )
    
    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', obj.resume.url)
        return "-"
    resume_link.short_description = 'Resume'
    
    def resume_preview(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank" class="button">Download Resume</a>', obj.resume.url)
        return "No resume uploaded"
    resume_preview.short_description = 'Resume File'
    
    def mark_under_review(self, request, queryset):
        updated = queryset.update(status='under_review')
        self.message_user(request, f'{updated} application(s) marked as Under Review.')
    mark_under_review.short_description = "Mark as Under Review"
    
    def mark_interview(self, request, queryset):
        updated = queryset.update(status='interview')
        self.message_user(request, f'{updated} application(s) marked as Interview Scheduled.')
    mark_interview.short_description = "Mark as Interview Scheduled"
    
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) marked as Rejected.')
    mark_rejected.short_description = "Mark as Rejected"
    
    def mark_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} application(s) marked as Accepted.')
    mark_accepted.short_description = "Mark as Accepted"


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'status', 'version', 'effective_date', 'last_updated')
    list_filter = ('page_type', 'status', 'effective_date')
    search_fields = ('title', 'slug', 'page_type')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('last_updated', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('page_type', 'title', 'slug', 'status')
        }),
        ('Version & Dates', {
            'fields': ('version', 'effective_date', 'last_updated', 'created_at')
        }),
        ('Content', {
            'fields': ('content_json',)
        }),
        ('Metadata', {
            'fields': ('meta_description', 'contact_email'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['publish_pages', 'unpublish_pages', 'archive_pages']
    
    def publish_pages(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} page(s) published successfully.')
    publish_pages.short_description = "Publish selected pages"
    
    def unpublish_pages(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} page(s) unpublished successfully.')
    unpublish_pages.short_description = "Unpublish selected pages"
    
    def archive_pages(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} page(s) archived successfully.')
    archive_pages.short_description = "Archive selected pages"


# ============================================================================
# AI Content Generation Admin
# ============================================================================

@admin.register(KeywordSource)
class KeywordSourceAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'source', 'status', 'priority', 'category', 'search_volume', 'viability_score', 'created_at']
    list_filter = ['status', 'source', 'priority', 'category', 'created_at']
    search_fields = ['keyword', 'notes']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'approved_by', 'approved_at', 'viability_score']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('keyword', 'source', 'category', 'status', 'priority')
        }),
        ('Metrics', {
            'fields': ('search_volume', 'competition', 'viability_score')
        }),
        ('AI Analysis', {
            'fields': ('suggested_angles', 'related_keywords', 'suggested_template'),
            'classes': ('collapse',)
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_at', 'rejected_reason')
        }),
        ('Additional', {
            'fields': ('notes', 'id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_keywords', 'reject_keywords']
    
    def approve_keywords(self, request, queryset):
        for keyword in queryset:
            keyword.approve(request.user)
        self.message_user(request, f'{queryset.count()} keyword(s) approved.')
    approve_keywords.short_description = "Approve selected keywords"
    
    def reject_keywords(self, request, queryset):
        updated = queryset.update(status=KeywordSource.Status.REJECTED)
        self.message_user(request, f'{updated} keyword(s) rejected.')
    reject_keywords.short_description = "Reject selected keywords"


@admin.register(AIArticle)
class AIArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'keyword', 'status', 'workflow_stage', 'overall_quality_score', 'created_at']
    list_filter = ['status', 'workflow_stage', 'template_type', 'created_at']
    search_fields = ['title', 'keyword__keyword']
    ordering = ['-created_at']
    readonly_fields = [
        'id', 'slug', 'actual_word_count', 'ai_score', 'plagiarism_score',
        'seo_score', 'readability_score', 'bias_score', 'fact_check_score',
        'overall_quality_score', 'generation_time', 'cost_estimate',
        'created_at', 'updated_at', 'generation_started_at', 'generation_completed_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('keyword', 'title', 'slug', 'template_type', 'status', 'workflow_stage')
        }),
        ('Content', {
            'fields': ('raw_content', 'content_json', 'target_word_count', 'actual_word_count'),
            'classes': ('collapse',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_title', 'meta_description', 'focus_keywords', 'og_title', 'og_description'),
            'classes': ('collapse',)
        }),
        ('Quality Scores', {
            'fields': (
                'ai_score', 'plagiarism_score', 'seo_score', 'readability_score',
                'bias_score', 'fact_check_score', 'overall_quality_score'
            )
        }),
        ('Media', {
            'fields': ('image_url', 'image_local_path', 'image_prompt', 'image_alt_text'),
            'classes': ('collapse',)
        }),
        ('Performance', {
            'fields': ('generation_time', 'cost_estimate', 'token_usage', 'ai_model_used'),
            'classes': ('collapse',)
        }),
        ('Error Tracking', {
            'fields': ('error_log', 'retry_count', 'last_error', 'failed_stage'),
            'classes': ('collapse',)
        }),
        ('Review', {
            'fields': ('reviewed_by', 'review_notes', 'published_article')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'generation_started_at', 'generation_completed_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AIGenerationConfig)
class AIGenerationConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'ai_provider', 'model_name', 'enabled', 'is_default']
    list_filter = ['template_type', 'ai_provider', 'enabled', 'is_default']
    search_fields = ['name', 'description']
    ordering = ['-is_default', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'template_type', 'enabled', 'is_default')
        }),
        ('AI Provider', {
            'fields': ('ai_provider', 'model_name')
        }),
        ('Prompts', {
            'fields': ('system_prompt', 'user_prompt_template', 'outline_prompt', 'research_prompt'),
            'classes': ('collapse',)
        }),
        ('Model Parameters', {
            'fields': ('temperature', 'max_tokens', 'top_p', 'frequency_penalty', 'presence_penalty')
        }),
        ('Content Settings', {
            'fields': (
                'target_word_count', 'num_headings',
                'include_statistics', 'include_quotes', 'include_internal_links'
            )
        }),
        ('Quality Thresholds', {
            'fields': (
                'max_ai_score', 'max_plagiarism_score', 'min_seo_score',
                'min_readability_score', 'max_bias_score'
            )
        }),
        ('Automation', {
            'fields': ('auto_humanize', 'auto_rewrite_plagiarism', 'auto_publish', 'max_retries')
        }),
        ('Metadata', {
            'fields': ('version', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AIWorkflowLog)
class AIWorkflowLogAdmin(admin.ModelAdmin):
    list_display = ['article', 'stage', 'status', 'execution_time', 'cost', 'timestamp']
    list_filter = ['stage', 'status', 'timestamp']
    search_fields = ['article__title', 'article__keyword__keyword']
    ordering = ['-timestamp']
    readonly_fields = ['id', 'timestamp', 'completed_at']
    
    fieldsets = (
        ('Article & Stage', {
            'fields': ('article', 'stage', 'status', 'retry_number', 'triggered_by')
        }),
        ('Data', {
            'fields': ('input_data', 'output_data'),
            'classes': ('collapse',)
        }),
        ('Error Information', {
            'fields': ('error_message', 'error_traceback'),
            'classes': ('collapse',)
        }),
        ('Performance', {
            'fields': ('execution_time', 'tokens_used', 'cost', 'ai_model')
        }),
        ('Timestamps', {
            'fields': ('timestamp', 'completed_at')
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Logs are created automatically
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete logs

