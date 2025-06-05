import unittest
from django.utils import timezone
from django.db import IntegrityError, DataError
from career.models import CareerAssessment
from users.models import Student

class CareerAssessmentModelTestCase(unittest.TestCase):
    def setUp(self):
        self.student = Student.objects.create_user(
            username='teststudent',
            password='password123',
            student_id='S12345',
            institution='Test University'
        )

    def tearDown(self):
        CareerAssessment.objects.all().delete()
        Student.objects.all().delete()

    def test_create_career_assessment_with_valid_data(self):
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
        assessment = CareerAssessment.objects.create(
            student=self.student,
            interests="math,science",
            skills="python,java",
            academic_strengths="algebra,geometry"
        )
        expected_str = f"Career Assessment for {self.student}"
        self.assertEqual(str(assessment), expected_str)

    def test_created_at_auto_now_add(self):
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
        with self.assertRaises(IntegrityError):
            CareerAssessment.objects.create(
                student=None,
                interests="math,science",
                skills="python,java",
                academic_strengths="algebra,geometry"
            )

    def test_career_assessment_with_empty_fields(self):
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

    