import unittest
from django.utils import timezone
from django.db import IntegrityError, DataError
from career.models import CareerAssessment, CareerRecommendation
from users.models import Student
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

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
class CareerRecommendationModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates a Student instance for use in CareerRecommendation tests.
        """
        self.student = Student.objects.create_user(
            username='teststudent',
            password='password123',
            student_id='S54321',
            institution='Test Institute'
        )

    def tearDown(self):
        """
        Cleans up CareerRecommendation and Student instances after each test.
        """
        CareerRecommendation.objects.all().delete()
        Student.objects.all().delete()

    def test_create_career_recommendation_success(self):
        """
        Tests successful creation of a CareerRecommendation with valid student and recommendation_text.
        """
        recommendation = CareerRecommendation.objects.create(
            student=self.student,
            recommendation_text="You should consider a career in engineering."
        )
        self.assertIsNotNone(recommendation.pk)
        self.assertEqual(recommendation.student, self.student)
        self.assertEqual(recommendation.recommendation_text, "You should consider a career in engineering.")

    def test_career_recommendation_str_representation(self):
        """
        Tests the __str__ method returns the expected string representation.
        """
        recommendation = CareerRecommendation.objects.create(
            student=self.student,
            recommendation_text="Explore data science."
        )
        expected_str = f"Career Recommendation for {self.student}"
        self.assertEqual(str(recommendation), expected_str)

    def test_career_recommendation_created_at_auto_now_add(self):
        """
        Tests that created_at is automatically set to the current datetime upon creation.
        """
        before = timezone.now()
        recommendation = CareerRecommendation.objects.create(
            student=self.student,
            recommendation_text="Try software development."
        )
        after = timezone.now()
        self.assertIsNotNone(recommendation.created_at)
        self.assertGreaterEqual(recommendation.created_at, before)
        self.assertLessEqual(recommendation.created_at, after)

    def test_career_recommendation_without_student_raises_error(self):
        """
        Tests that creating a CareerRecommendation without a student raises an IntegrityError.
        """
        with self.assertRaises(IntegrityError):
            CareerRecommendation.objects.create(
                student=None,
                recommendation_text="Consider teaching."
            )

    def test_career_recommendation_empty_recommendation_text(self):
        """
        Tests that creating a CareerRecommendation with an empty recommendation_text is allowed.
        """
        recommendation = CareerRecommendation.objects.create(
            student=self.student,
            recommendation_text=""
        )
        self.assertEqual(recommendation.recommendation_text, "")

    def test_career_recommendation_cascade_delete_on_student_removal(self):
        """
        Tests that deleting a Student cascades and deletes associated CareerRecommendation instances.
        """
        recommendation = CareerRecommendation.objects.create(
            student=self.student,
            recommendation_text="Consider entrepreneurship."
        )
        self.student.delete()
        self.assertFalse(CareerRecommendation.objects.filter(pk=recommendation.pk).exists())

    def test_retrieve_career_recommendation_from_db(self):
        """
        Tests that a CareerRecommendation instance can be retrieved from the database after being saved.
        """
        recommendation = CareerRecommendation.objects.create(
            student=self.student,
            recommendation_text="Explore research roles."
        )
        retrieved = CareerRecommendation.objects.get(pk=recommendation.pk)
        self.assertEqual(retrieved, recommendation)
        self.assertEqual(retrieved.student, self.student)
        self.assertEqual(retrieved.recommendation_text, "Explore research roles.")

    def test_career_recommendation_invalid_student_fk_raises_error(self):
        """
        Tests that creating a CareerRecommendation with a non-existent Student foreign key raises an IntegrityError.
        """
        invalid_student_id = self.student.pk
        self.student.delete()
        with self.assertRaises(IntegrityError):
            CareerRecommendation.objects.create(
                student_id=invalid_student_id,
                recommendation_text="Try consulting."
            )
            
# class CareerRecommendationViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user1 = User.objects.create_user(username='student1', password='testpass1')
#         self.user2 = User.objects.create_user(username='student2', password='testpass2')
#         self.recommendation1 = CareerRecommendation.objects.create(
#             student=self.user1,
#             recommendation_text="Recommendation for user1 - 1"
#         )
#         self.recommendation2 = CareerRecommendation.objects.create(
#             student=self.user1,
#             recommendation_text="Recommendation for user1 - 2"
#         )
#         self.recommendation3 = CareerRecommendation.objects.create(
#             student=self.user2,
#             recommendation_text="Recommendation for user2"
#         )
#         self.list_url = reverse('careerrecommendation-list')

#     def test_user_retrieves_own_career_recommendations(self):
#         """
#         Authenticated user retrieves only their own career recommendations.
#         """
#         self.client.login(username='student1', password='testpass1')
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         ids = [rec['id'] for rec in response.json()]
#         expected_ids = list(CareerRecommendation.objects.filter(student=self.user1).values_list('id', flat=True))
#         self.assertCountEqual(ids, expected_ids)
#         for rec in response.json():
#             self.assertEqual(rec['student'], self.user1.id)

#     def test_user_with_no_recommendations_receives_empty_list(self):
#         """
#         Authenticated user receives an empty list when they have no career recommendations.
#         """
#         user3 = User.objects.create_user(username='student3', password='testpass3')
#         self.client.login(username='student3', password='testpass3')
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), [])

#     def test_recommendation_serialization_includes_all_fields(self):
#         """
#         Authenticated user receives recommendations serialized with all model fields.
#         """
#         self.client.login(username='student1', password='testpass1')
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         for rec in response.json():
#             self.assertIn('id', rec)
#             self.assertIn('student', rec)
#             self.assertIn('recommendation_text', rec)
#             self.assertIn('created_at', rec)

#     def test_unauthenticated_user_access_denied(self):
#         """
#         Unauthenticated user is denied access to the career recommendations endpoint.
#         """
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 403)

#     def test_user_cannot_access_others_recommendations(self):
#         """
#         Authenticated user attempts to access another user's career recommendations.
#         """
#         self.client.login(username='student2', password='testpass2')
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         for rec in response.json():
#             self.assertEqual(rec['student'], self.user2.id)
#         ids = [rec['id'] for rec in response.json()]
#         self.assertNotIn(self.recommendation1.id, ids)
#         self.assertNotIn(self.recommendation2.id, ids)

#     def test_handling_of_malformed_recommendation_data(self):
#         """
#         CareerRecommendation model contains recommendations with missing or malformed data.
#         """
#         # Create a recommendation with empty recommendation_text (allowed by model)
#         malformed = CareerRecommendation.objects.create(
#             student=self.user1,
#             recommendation_text=""
#         )
#         self.client.login(username='student1', password='testpass1')
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         found = False
#         for rec in response.json():
#             if rec['id'] == malformed.id:
#                 found = True
#                 self.assertEqual(rec['recommendation_text'], "")
#         self.assertTrue(found)

#     def test_recommendations_are_ordered_by_created_at(self):
#         """
#         Authenticated user receives career recommendations ordered by creation date.
#         """
#         self.client.login(username='student1', password='testpass1')
#         # Create a new recommendation to ensure ordering
#         rec_new = CareerRecommendation.objects.create(
#             student=self.user1,
#             recommendation_text="Newest recommendation"
#         )
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, 200)
#         recs = response.json()
#         created_ats = [rec['created_at'] for rec in recs]
#         # Should be ordered by created_at ascending (oldest first)
#         self.assertEqual(created_ats, sorted(created_ats))

#     def test_database_error_handling_on_recommendation_retrieval(self):
#         """
#         Database error occurs while retrieving career recommendations.
#         """
#         # Simulate DB error by deleting all recommendations and the user, then querying as that user
#         self.client.login(username='student1', password='testpass1')
#         CareerRecommendation.objects.all().delete()
#         # Drop the table to simulate a DB error (not recommended in real tests, but no mocks allowed)
#         from django.db import connection
#         with connection.cursor() as cursor:
#             cursor.execute('DROP TABLE career_careerrecommendation')
#         response = self.client.get(self.list_url)
#         self.assertIn(response.status_code, (500, 503, 400))