from django.contrib import admin
from .models import News, TeamMember
from django.utils.html import format_html

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'preview_image')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__name')
    fields = ('title', 'content', 'category', 'author', 'image', 'preview_image_display')
    readonly_fields = ('preview_image_display',)

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


