from rest_framework import serializers
from .legal_models import LegalPage


class LegalPageSerializer(serializers.ModelSerializer):
    """Serializer for Legal Pages"""
    
    page_type_display = serializers.CharField(source='get_page_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = LegalPage
        fields = [
            'id',
            'page_type',
            'page_type_display',
            'title',
            'slug',
            'content_json',
            'status',
            'status_display',
            'version',
            'effective_date',
            'last_updated',
            'created_at',
            'meta_description',
            'contact_email',
        ]
        read_only_fields = ['last_updated', 'created_at']
    
    def validate_content_json(self, value):
        """Validate that content_json has required structure"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Content must be a valid JSON object")
        
        # Check for required fields based on page type
        if 'metadata' not in value:
            raise serializers.ValidationError("Content must include 'metadata' section")
        
        return value
    
    def validate_slug(self, value):
        """Ensure slug is unique"""
        if self.instance:
            # Update case - exclude current instance
            if LegalPage.objects.exclude(pk=self.instance.pk).filter(slug=value).exists():
                raise serializers.ValidationError("This slug is already in use")
        else:
            # Create case
            if LegalPage.objects.filter(slug=value).exists():
                raise serializers.ValidationError("This slug is already in use")
        return value


class LegalPageListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing legal pages"""
    
    page_type_display = serializers.CharField(source='get_page_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = LegalPage
        fields = [
            'id',
            'page_type',
            'page_type_display',
            'title',
            'slug',
            'status',
            'status_display',
            'version',
            'effective_date',
            'last_updated',
        ]
