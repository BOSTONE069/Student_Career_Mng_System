import unittest
from django.utils import timezone
from django.db import IntegrityError, DataError
from career.models import CareerAssessment
from users.models import Student

class CareerAssessmentModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        The setUp function creates a student user with specified details in a Python test case.
        """
        self.student = Student.objects.create_user(
            username='teststudent',
            password='password123',
            student_id='S12345',
            institution='Test University'
        )

    def tearDown(self):
        """
        The `tearDown` function deletes all instances of `CareerAssessment` and `Student` objects from
        the database.
        """
        CareerAssessment.objects.all().delete()
        Student.objects.all().delete()

    def test_create_career_assessment_with_valid_data(self):
        """
        The function `test_create_career_assessment_with_valid_data` creates a CareerAssessment object
        with specific data and asserts its attributes.
        """
        assessment = CareerAssessment.objects.create(
            student=self.student,
            interests="math,science",
            skills="python,java",
            academic_strengths="algebra,geometry"
        )
        self.assertIsNotNone(assessment.pk)
        self.assertEqual(assessment.student, self.student)
        self.assertEqual(assessment.interests, "math,science")
        self.assertEqual(assessment.skills, "python,java")
        self.assertEqual(assessment.academic_strengths, "algebra,geometry")

    def test_career_assessment_str_representation(self):
        """
        The function creates a CareerAssessment object and tests its string representation.
        """
        assessment = CareerAssessment.objects.create(
            student=self.student,
            interests="math,science",
            skills="python,java",
            academic_strengths="algebra,geometry"
        )
        expected_str = f"Career Assessment for {self.student}"
        self.assertEqual(str(assessment), expected_str)

    def test_created_at_auto_now_add(self):
        """
        The function tests if the 'created_at' field of a CareerAssessment object is automatically set
        to the current time upon creation.
        """
        before = timezone.now()
        assessment = CareerAssessment.objects.create(
            student=self.student,
            interests="math,science",
            skills="python,java",
            academic_strengths="algebra,geometry"
        )
        after = timezone.now()
        self.assertIsNotNone(assessment.created_at)
        self.assertGreaterEqual(assessment.created_at, before)
        self.assertLessEqual(assessment.created_at, after)

    def test_career_assessment_without_student(self):
        """
        The function tests the creation of a CareerAssessment object without a student, expecting an
        IntegrityError to be raised.
        """
        with self.assertRaises(IntegrityError):
            CareerAssessment.objects.create(
                student=None,
                interests="math,science",
                skills="python,java",
                academic_strengths="algebra,geometry"
            )

    def test_career_assessment_with_empty_fields(self):
        """
        The function tests the creation of a CareerAssessment object with empty fields for interests,
        skills, and academic strengths.
        """
        assessment = CareerAssessment.objects.create(
            student=self.student,
            interests="",
            skills="",
            academic_strengths=""
        )
        self.assertEqual(assessment.interests, "")
        self.assertEqual(assessment.skills, "")
        self.assertEqual(assessment.academic_strengths, "")

    def test_cascade_delete_on_student_removal(self):
        """
        The function tests cascade deletion on the removal of a student by creating a CareerAssessment
        instance associated with the student and then deleting the student to verify if the
        CareerAssessment instance is also deleted.
        """
        assessment = CareerAssessment.objects.create(
            student=self.student,
            interests="math,science",
            skills="python,java",
            academic_strengths="algebra,geometry"
        )
        self.student.delete()
        self.assertFalse(CareerAssessment.objects.filter(pk=assessment.pk).exists())

    def test_update_career_assessment_fields(self):
        assessment = CareerAssessment.objects.create(
            student=self.student,
            interests="math,science",
            skills="python,java",
            academic_strengths="algebra,geometry"
        )
        assessment.interests = "history,art"
        assessment.skills = "c++,go"
        assessment.academic_strengths = "literature,philosophy"
        assessment.save()
        updated = CareerAssessment.objects.get(pk=assessment.pk)
        self.assertEqual(updated.interests, "history,art")
        self.assertEqual(updated.skills, "c++,go")
        self.assertEqual(updated.academic_strengths, "literature,philosophy")

    