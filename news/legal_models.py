from django.db import models
from django.utils import timezone


class LegalPage(models.Model):
    """Model for legal/administrative pages like Privacy Policy, Terms of Service, etc."""
    
    PAGE_TYPES = [
        ('privacy_policy', 'Privacy Policy'),
        ('terms_of_service', 'Terms of Service'),
        ('cookie_policy', 'Cookie Policy'),
        ('ethics_policy', 'Ethics Policy'),
        ('editorial_guidelines', 'Editorial Guidelines'),
        ('about', 'About Us'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    page_type = models.CharField(
        max_length=50,
        choices=PAGE_TYPES,
        unique=True,
        help_text="Type of legal/administrative page"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content_json = models.JSONField(
        help_text="JSON structure containing the page content"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    version = models.CharField(max_length=20, default='1.0')
    effective_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metadata
    meta_description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    
    class Meta:
        ordering = ['-last_updated']
        verbose_name = 'Legal Page'
        verbose_name_plural = 'Legal Pages'
    
    def __str__(self):
        return f"{self.get_page_type_display()} - v{self.version}"
    
    def save(self, *args, **kwargs):
        # Auto-update last_updated timestamp
        if not self.pk:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)
