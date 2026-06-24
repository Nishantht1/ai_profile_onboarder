from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class JobSeekerProfile(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('reviewed', 'Reviewed'),
        ('open_to_work', 'Open to Work'),
        ('not_interested','Not Interested'),

    ]

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    dob= models.DateField(blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    aadhar_number = models.CharField(max_length=20, blank=True, null=True)
    current_city = models.CharField(max_length=100, blank=True, null=True)
    preferred_city = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    experience_type = models.CharField(max_length=50, blank=True, null=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    current_company = models.CharField(max_length=150, blank=True, null=True)
    experience_summary = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='created')


    def __str__(self):
        return self.user.email
    
class ProjectHistory(models.Model):
        profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='projects')
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True, null=True)
        duration_from = models.CharField(max_length=50, blank=True, null=True)
        duration_to = models.CharField(max_length=50, blank=True, null=True)
        role = models.CharField(max_length=100, blank=True, null=True)
        activities = models.TextField(blank=True, null=True)

        def __str__(self):
            return self.title


class Skill(models.Model):
    profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Certification(models.Model):
    profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issued_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Award(models.Model):
    profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title