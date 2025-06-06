from django.db import models
from django.conf import settings
from django.db.models import Q, CheckConstraint

class ExamRegistration(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    registered_on = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(year__gt=0), name='year_positive')
        ]

    def __str__(self):
        return f"{self.student.username} - {self.course_code}"
