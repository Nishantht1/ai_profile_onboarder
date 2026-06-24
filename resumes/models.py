from django.db import models

# Create your models here.
from profiles.models import JobSeekerProfile


class Resume(models.Model):
    PARSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    profile = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name='resumes',
        blank=True,
        null=True
    )

    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_text = models.TextField(blank=True, null=True)
    parsing_status = models.CharField(
        max_length=20,
        choices=PARSING_STATUS_CHOICES,
        default='pending'
    )

    llm_response = models.JSONField(null=True, blank=True)


    def __str__(self):
        return self.file.name