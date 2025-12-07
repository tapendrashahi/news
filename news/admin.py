from django.contrib import admin
from .models import News, TeamMember, Comment, ShareCount, JobOpening, JobApplication
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


