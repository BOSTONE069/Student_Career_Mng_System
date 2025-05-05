from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True)
    institution = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.student_id})"
