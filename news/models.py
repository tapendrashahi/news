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

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='business')
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', help_text="Select the author from team members")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    def __str__(self):
        return self.title

