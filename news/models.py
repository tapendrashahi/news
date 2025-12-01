from django.db import models

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('editor_in_chief', 'Editor-in-Chief'),
        ('tech_editor', 'Tech Editor'),
        ('political_analyst', 'Political Analyst'),
        ('business_reporter', 'Business Reporter'),
        ('sports_reporter', 'Sports Reporter'),
        ('senior_editor', 'Senior Editor'),
        ('staff_writer', 'Staff Writer'),
        ('photographer', 'Photographer'),
        ('video_journalist', 'Video Journalist'),
    ]

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, help_text="Brief biography of the team member")
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True, help_text="Professional headshot")
    email = models.EmailField(blank=True, help_text="Professional email address")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    is_active = models.BooleanField(default=True, help_text="Is this team member currently active?")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    joined_date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
    
    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"


class News(models.Model):
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('political', 'Political'),
        ('tech', 'Tech'),
        ('education', 'Education'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('password', 'Password Protected'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, help_text="URL-friendly version of title")
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief summary of the article")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='business')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', help_text="Select the author from team members")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    publish_date = models.DateTimeField(null=True, blank=True, help_text="Schedule publish date/time")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News Article'
        verbose_name_plural = 'News Articles'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while News.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, help_text="Commenter's name")
    email = models.EmailField(help_text="Commenter's email (not displayed publicly)")
    text = models.TextField(help_text="Comment text")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, help_text="Whether this comment is approved for display")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f"Comment by {self.name} on {self.news.title}"


class ShareCount(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('email', 'Email'),
    ]
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='shares')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    count = models.IntegerField(default=0)
    last_shared = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['news', 'platform']
        verbose_name = 'Share Count'
        verbose_name_plural = 'Share Counts'
    
    def __str__(self):
        return f"{self.news.title} - {self.platform}: {self.count}"


class Subscriber(models.Model):
    """Newsletter subscriber model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True, help_text="Whether subscriber is active")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
    
    def __str__(self):
        return self.email

