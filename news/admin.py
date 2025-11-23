from django.contrib import admin
from .models import News
from django.utils.html import format_html

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'preview_image')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    fields = ('title', 'content', 'category', 'image', 'preview_image_display')
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

