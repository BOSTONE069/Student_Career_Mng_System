from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from users.models import Student

# Create your tests here.

class StudentModelTest(TestCase):
    def test_create_student_with_valid_data(self):
        """
        The function tests the creation of a student object with valid data.
        """
        student = Student.objects.create_user(
            username='testuser',
            password='testpass123',
            student_id='S123456',
            institution='Test University'
        )
        self.assertIsNotNone(student.pk)
        self.assertEqual(student.username, 'testuser')
        self.assertEqual(student.student_id, 'S123456')
        self.assertEqual(student.institution, 'Test University')

    def test_student_str_representation(self):
        """
        The function creates a student object and tests its string representation.
        """
        student = Student.objects.create_user(
            username='john_doe',
            password='testpass123',
            student_id='JD2024'
        )
        self.assertEqual(str(student), "john_doe (JD2024)")

    def test_create_student_without_institution(self):
        """
        The function tests creating a student without an institution in Python.
        """
        student = Student.objects.create_user(
            username='noinst',
            password='testpass123',
            student_id='N123'
        )
        self.assertIsNone(student.institution)
        self.assertEqual(student.student_id, 'N123')

    def test_duplicate_student_id_raises_error(self):
        """
        The function tests that creating a student with a duplicate student ID raises an IntegrityError.
        """
        Student.objects.create_user(
            username='user1',
            password='testpass123',
            student_id='DUPLICATE'
        )
        with self.assertRaises(IntegrityError):
            Student.objects.create_user(
                username='user2',
                password='testpass123',
                student_id='DUPLICATE'
            )

    def test_student_id_max_length_validation(self):
        """
        The function tests the validation of the maximum length of a student ID in a Student object.
        """
        student = Student(
            username='longid',
            student_id='X' * 21  # max_length is 20
        )
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_student_id_null_raises_error(self):
        """
        The function tests that a ValidationError is raised when a Student instance with a null student
        ID is validated.
        """
        student = Student(
            username='nullid',
            student_id=None
        )
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_update_student_institution(self):
        """
        The function creates a student object, updates its institution attribute, saves the changes, and
        then retrieves the updated student to assert that the institution has been successfully updated.
        """
        student = Student.objects.create_user(
            username='updateinst',
            password='testpass123',
            student_id='U123'
        )
        student.institution = 'Updated Institution'
        student.save()
        updated = Student.objects.get(pk=student.pk)
        self.assertEqual(updated.institution, 'Updated Institution')

    def test_institution_max_length_validation(self):
        """
        The function tests the maximum length validation for the institution field of a Student object.
        """
        student = Student(
            username='longinst',
            student_id='L123',
            institution='A' * 101  # max_length is 100
        )
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_student_inherits_abstractuser_fields(self):
        """
        The function tests if a Student model inherits fields from AbstractUser in Django.
        """
        student = Student.objects.create_user(
            username='inherituser',
            password='testpass123',
            student_id='INH123'
        )
        # Check for some AbstractUser fields
        self.assertTrue(hasattr(student, 'last_login'))
        self.assertTrue(hasattr(student, 'is_superuser'))
        self.assertTrue(hasattr(student, 'email'))
        self.assertTrue(hasattr(student, 'is_active'))
        self.assertTrue(hasattr(student, 'date_joined'))

    def test_blank_student_id_raises_validation_error(self):
        """
        The function tests that a blank student ID raises a validation error when creating a Student
        instance.
        """
        student = Student(
            username='blankid',
            student_id=''
        )
        with self.assertRaises(ValidationError):
            student.full_clean()