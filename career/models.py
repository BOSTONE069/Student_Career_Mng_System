from django.db import models
from users.models import Student

class CareerAssessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    interests = models.TextField(help_text="Comma-separated interests")
    skills = models.TextField(help_text="Comma-separated skills")
    academic_strengths = models.TextField(help_text="Comma-separated subjects")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Career Assessment for {self.student}"

class CareerRecommendation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    recommendation_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Career Recommendation for {self.student}"
