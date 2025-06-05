from django.db import models

from django.core.exceptions import ValidationError

# The `Institution` class defines a model with fields for name, code, and website URL in a Django
# application.
class Institution(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# The `Program` class represents a program offered by an institution with attributes such as name,
# duration in years, and a reference to the institution.
class Program(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration_years = models.PositiveIntegerField(
        verbose_name="Duration (Years)",
        help_text="Enter number of years. Must be at least 1."
    )

    def __str__(self):
        return f"{self.name} - {self.institution.name}"

    def clean(self):
        if self.duration_years <= 0:
            raise ValidationError({
                'duration_years': 'Duration in years must be greater than zero.'
            })


# The `Course` class represents a course with a title, semester, and a foreign key reference to a
# `Program` object.
class Course(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    semester = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} - {self.program.name}"


# The `Unit` class represents a unit within a course with attributes such as code, name, and
# description.
class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


# The `Fee` class represents a fee associated with a program, including details such as amount,
# currency, fee type, and description.
class Fee(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='KSH')
    fee_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fee_type} - {self.amount} {self.currency} for {self.program.name}"
    
