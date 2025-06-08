from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import IntegrityError, DataError
from ExamRegistration.models import ExamRegistration
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from django.db import transaction

User = get_user_model()

class ExamRegistrationModelTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='teststudent', password='testpass', student_id='S1001')

    def test_create_exam_registration_success(self):
        """
        The function `test_create_exam_registration_success` creates an exam registration object with
        specific attributes and asserts its correctness.
        """
        reg = ExamRegistration.objects.create(
            student=self.student,
            course_code='CS101',
            course_title='Intro to Computer Science',
            semester='Fall',
            year=2024
        )
        self.assertIsInstance(reg, ExamRegistration)
        self.assertEqual(reg.student, self.student)
        self.assertEqual(reg.course_code, 'CS101')
        self.assertEqual(reg.course_title, 'Intro to Computer Science')
        self.assertEqual(reg.semester, 'Fall')
        self.assertEqual(reg.year, 2024)

    def test_registered_on_auto_now_add(self):
        """
        The function tests if the 'registered_on' field in an ExamRegistration object is set to the
        current time with a tolerance of 5 seconds.
        """
        reg = ExamRegistration.objects.create(
            student=self.student,
            course_code='CS102',
            course_title='Data Structures',
            semester='Spring',
            year=2024
        )
        now = timezone.now()
        self.assertIsNotNone(reg.registered_on)
        self.assertLessEqual(abs((now - reg.registered_on).total_seconds()), 5)

    def test_is_verified_default_false(self):
        """
        The function creates an ExamRegistration object with default is_verified value set to False and
        asserts that it is indeed False.
        """
        reg = ExamRegistration.objects.create(
            student=self.student,
            course_code='CS103',
            course_title='Algorithms',
            semester='Summer',
            year=2024
        )
        self.assertFalse(reg.is_verified)

    # This test function `test_missing_required_field_raises_error` is checking if a `ValidationError`
    # is raised when trying to save an `ExamRegistration` instance with a missing required field
    # (`course_code` in this case).
    def test_missing_required_field_raises_error(self):
        reg = ExamRegistration(
            student=self.student,
            # course_code is missing
            course_title='Networks',
            semester='Fall',
            year=2024
        )
        with self.assertRaises(ValidationError):
            reg.full_clean()
            reg.save()

    def test_year_positive_integer_constraint(self):
        """
        The function tests the positive integer constraint for the 'year' field in an ExamRegistration
        model.
        """
        reg_zero = ExamRegistration(
            student=self.student,
            course_code='CS104',
            course_title='Operating Systems',
            semester='Winter',
            year=0
        )
        reg_negative = ExamRegistration(
            student=self.student,
            course_code='CS105',
            course_title='Databases',
            semester='Winter',
            year=-2024
        )
        with self.assertRaises(ValidationError):
            reg_zero.full_clean()
        with self.assertRaises(ValidationError):
            reg_negative.full_clean()

    def test_cascade_delete_on_student_removal(self):
        """
        The above functions test cascade delete behavior on student removal, string representation of
        exam registration, and max length constraints on fields in a Django model.
        """
        reg = ExamRegistration.objects.create(
            student=self.student,
            course_code='CS106',
            course_title='AI',
            semester='Spring',
            year=2024
        )
        self.student.delete()
        self.assertFalse(ExamRegistration.objects.filter(pk=reg.pk).exists())

    def test_exam_registration_str_representation(self):
        reg = ExamRegistration.objects.create(
            student=self.student,
            course_code='CS107',
            course_title='ML',
            semester='Fall',
            year=2024
        )
        expected_str = f"{self.student.username} - CS107"
        self.assertEqual(str(reg), expected_str)

    def test_max_length_constraints_on_fields(self):
        long_code = 'C' * 21  # max_length=20
        long_title = 'T' * 101  # max_length=100
        with self.assertRaises(DataError):
            with transaction.atomic():
                ExamRegistration.objects.create(
                    student=self.student,
                    course_code=long_code,
                    course_title='Valid Title',
                    semester='Fall',
                    year=2024
                )
        with self.assertRaises(DataError):
            with transaction.atomic():
                ExamRegistration.objects.create(
                    student=self.student,
                    course_code='CS108',
                    course_title=long_title,
                    semester='Fall',
                    year=2024
                )

    def test_filter_exam_registrations_by_student(self):
        """
        The function `test_filter_exam_registrations_by_student` creates exam registrations for two
        students and then filters them by a specific student, asserting that only the correct
        registrations are returned.
        """
        other_student = User.objects.create_user(username='otherstudent', password='otherpass', student_id='S1002')
        reg1 = ExamRegistration.objects.create(
            student=self.student,
            course_code='CS109',
            course_title='Security',
            semester='Spring',
            year=2024
        )
        reg2 = ExamRegistration.objects.create(
            student=other_student,
            course_code='CS110',
            course_title='Graphics',
            semester='Spring',
            year=2024
        )
        regs = ExamRegistration.objects.filter(student=self.student)
        self.assertIn(reg1, regs)
        self.assertNotIn(reg2, regs)
        self.assertEqual(regs.count(), 1)

    def test_create_with_invalid_student_reference(self):
        """
        The function tests creating an exam registration with an invalid student reference.
        """
        """
        The function tests creating an exam registration with an invalid student reference.
        """
        invalid_pk = self.student.pk + 1000
        reg = ExamRegistration(
            student_id=invalid_pk,
            course_code='CS111',
            course_title='Quantum Computing',
            semester='Fall',
            year=2024
        )
        with self.assertRaises(ValidationError):
            reg.full_clean()
            reg.save()
