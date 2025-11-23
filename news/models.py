from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    def __str__(self):
        return self.title
