from django.db import models
from django.conf import settings

class Institution(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.institution.name}"


class Course(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    semester = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} - {self.program.name}"


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Fee(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    fee_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fee_type} - {self.amount} {self.currency} for {self.program.name}"
    
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
