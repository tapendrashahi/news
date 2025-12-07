from django.db import models
from django.core.validators import FileExtensionValidator

class JobOpening(models.Model):
    DEPARTMENT_CHOICES = [
        ('editorial', 'Editorial'),
        ('technology', 'Technology'),
        ('business', 'Business'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead'),
    ]
    
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    location = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES)
    description = models.TextField()
    responsibilities = models.TextField(help_text="Enter one responsibility per line")
    requirements = models.TextField(help_text="Enter one requirement per line")
    salary_range = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    application_deadline = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-posted_date']
        verbose_name = 'Job Opening'
        verbose_name_plural = 'Job Openings'
    
    def __str__(self):
        return f"{self.title} - {self.department}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    resume = models.FileField(
        upload_to='resumes/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text="Upload resume in PDF, DOC, or DOCX format (Max 5MB)"
    )
    cover_letter = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Admin notes")
    
    class Meta:
        ordering = ['-applied_date']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
    
    def __str__(self):
        return f"{self.full_name} - {self.job_opening.title}"
