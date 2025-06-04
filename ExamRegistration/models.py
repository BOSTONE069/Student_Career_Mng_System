from django.db import models
from django.conf import settings

class ExamRegistration(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    registered_on = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.course_code}"
