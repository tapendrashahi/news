from rest_framework import serializers
from .models import News, TeamMember, Comment, ShareCount, Subscriber, JobOpening, JobApplication


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for TeamMember model"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamMember
        fields = [
            'id', 'name', 'role', 'role_display', 'bio', 'photo',
            'email', 'twitter_url', 'linkedin_url', 'is_active',
            'order', 'joined_date', 'article_count'
        ]
    
    def get_article_count(self, obj):
        """Get count of articles written by this team member"""
        return obj.articles.count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    
    class Meta:
        model = Comment
        fields = ['id', 'news', 'name', 'email', 'text', 'created_at', 'is_approved']
        read_only_fields = ['created_at', 'is_approved']
        extra_kwargs = {
            'news': {'required': False}  # Make news optional for creation via action
        }
    
    def validate_text(self, value):
        """Validate comment text"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Comment must be at least 3 characters long.")
        return value


class CommentListSerializer(serializers.ModelSerializer):
    """Serializer for listing comments (excludes email)"""
    
    class Meta:
        model = Comment
        fields = ['id', 'name', 'text', 'created_at', 'is_approved']


class ShareCountSerializer(serializers.ModelSerializer):
    """Serializer for ShareCount model"""
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = ShareCount
        fields = ['id', 'platform', 'platform_display', 'count', 'last_shared']


class NewsListSerializer(serializers.ModelSerializer):
    """Serializer for listing news articles (summary view)"""
    author = TeamMemberSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    comment_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'excerpt', 'category', 'category_display',
            'author', 'image', 'created_at', 'updated_at', 'publish_date',
            'comment_count', 'share_count', 'tags_list'
        ]
    
    def get_comment_count(self, obj):
        """Get count of approved comments"""
        return obj.comments.filter(is_approved=True).count()
    
    def get_share_count(self, obj):
        """Get total share count across all platforms"""
        return sum(share.count for share in obj.shares.all())
    
    def get_tags_list(self, obj):
        """Get tags as a list"""
        return obj.get_tags_list()


class NewsDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed news article view"""
    author = TeamMemberSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)
    shares = ShareCountSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    total_shares = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    related_news = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'category', 
            'category_display', 'author', 'image', 'created_at', 'updated_at',
            'publish_date', 'meta_description', 'tags', 'tags_list',
            'comments', 'comment_count', 'shares', 'total_shares', 'related_news'
        ]
    
    def get_comment_count(self, obj):
        """Get count of approved comments"""
        return obj.comments.filter(is_approved=True).count()
    
    def get_total_shares(self, obj):
        """Get total share count across all platforms"""
        return sum(share.count for share in obj.shares.all())
    
    def get_tags_list(self, obj):
        """Get tags as a list"""
        return obj.get_tags_list()
    
    def get_related_news(self, obj):
        """Get related news articles from the same category"""
        related = News.objects.filter(
            category=obj.category,
            visibility='public'
        ).exclude(id=obj.id).order_by('-created_at')[:3]
        
        return NewsListSerializer(related, many=True, context=self.context).data


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating news articles"""
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'category',
            'tags', 'author', 'meta_description', 'visibility',
            'publish_date', 'image'
        ]
    
    def validate_title(self, value):
        """Validate title"""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
    
    def validate_content(self, value):
        """Validate content"""
        if len(value.strip()) < 50:
            raise serializers.ValidationError("Content must be at least 50 characters long.")
        return value


class SubscriberSerializer(serializers.ModelSerializer):
    """Serializer for newsletter subscribers"""
    
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'name', 'is_active', 'subscribed_at']
        read_only_fields = ['subscribed_at']
    
    def validate_email(self, value):
        """Validate email"""
        # Check if email already exists and is active
        if self.instance is None:  # Creating new subscriber
            existing = Subscriber.objects.filter(email=value, is_active=True).first()
            if existing:
                raise serializers.ValidationError("This email is already subscribed.")
        return value


class CategorySerializer(serializers.Serializer):
    """Serializer for category information"""
    name = serializers.CharField()
    display_name = serializers.CharField()
    count = serializers.IntegerField()
    description = serializers.CharField(required=False)


class JobOpeningSerializer(serializers.ModelSerializer):
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    employment_type_display = serializers.CharField(source='get_employment_type_display', read_only=True)
    experience_level_display = serializers.CharField(source='get_experience_level_display', read_only=True)
    application_count = serializers.SerializerMethodField()
    responsibilities_list = serializers.SerializerMethodField()
    requirements_list = serializers.SerializerMethodField()
    
    class Meta:
        model = JobOpening
        fields = [
            'id', 'title', 'department', 'department_display', 'location',
            'employment_type', 'employment_type_display', 'experience_level',
            'experience_level_display', 'description', 'responsibilities',
            'responsibilities_list', 'requirements', 'requirements_list',
            'salary_range', 'is_active', 'posted_date', 'application_deadline',
            'application_count'
        ]
    
    def get_application_count(self, obj):
        return obj.applications.count()
    
    def get_responsibilities_list(self, obj):
        return [r.strip() for r in obj.responsibilities.split('\n') if r.strip()]
    
    def get_requirements_list(self, obj):
        return [r.strip() for r in obj.requirements.split('\n') if r.strip()]


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job_opening.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job_opening', 'job_title', 'full_name', 'email', 'phone',
            'linkedin_url', 'portfolio_url', 'resume', 'cover_letter',
            'years_of_experience', 'status', 'status_display', 'applied_date'
        ]
        read_only_fields = ['id', 'status', 'applied_date']
    
    def validate_resume(self, value):
        # Validate file size (5MB max)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Resume file size cannot exceed 5MB.")
        return value

