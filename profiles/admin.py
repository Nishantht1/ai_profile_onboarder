from django.contrib import admin

# Register your models here.
from .models import JobSeekerProfile, ProjectHistory, Skill, Certification, Award


admin.site.register(JobSeekerProfile)
admin.site.register(ProjectHistory)
admin.site.register(Skill)
admin.site.register(Certification)
admin.site.register(Award)