from django.test import TestCase
from django.db import IntegrityError, DataError
from academics.models import Institution, Program
from django.core.exceptions import ValidationError
# Create your tests here.

class InstitutionModelTest(TestCase):
    def test_create_institution_with_valid_fields(self):
        """
        The function tests the creation of an Institution object with valid fields.
        """
        institution = Institution.objects.create(
            name="Test University",
            code="TU123",
            website="https://www.testuniversity.edu"
        )
        self.assertEqual(institution.name, "Test University")
        self.assertEqual(institution.code, "TU123")
        self.assertEqual(institution.website, "https://www.testuniversity.edu")

    def test_institution_str_returns_name(self):
        """
        The function tests that the `__str__` method of an Institution object returns its name.
        """
        institution = Institution.objects.create(
            name="Sample College",
            code="SC001"
        )
        self.assertEqual(str(institution), "Sample College")

    def test_create_institution_without_website(self):
        """
        The function creates an Institution object without a website and asserts that the website
        attribute is None.
        """
        institution = Institution.objects.create(
            name="No Website Institute",
            code="NWI001"
        )
        self.assertIsNone(institution.website)

    def test_institution_code_uniqueness_constraint(self):
        """
        The function tests the uniqueness constraint of the institution code field in a Django model.
        """
        Institution.objects.create(
            name="First Institute",
            code="UNIQUE01"
        )
        with self.assertRaises(IntegrityError):
            Institution.objects.create(
                name="Second Institute",
                code="UNIQUE01"
            )
    def test_institution_name_max_length_exceeded(self):
        """
        The function tests if an error is raised when creating an Institution object with a name
        exceeding the maximum length.
        """
        long_name = "A" * 256  # max_length is 255
        with self.assertRaises(DataError):
            Institution.objects.create(
                name=long_name,
                code="LONGNAME01"
            )

    def test_institution_creation_with_valid_data(self):
        """
        The function tests the creation of an Institution object with valid data.
        """
        institution = Institution.objects.create(
            name="Valid Data Institute",
            code="VDI001",
            website="https://www.validdatainstitute.com"
        )
        self.assertTrue(Institution.objects.filter(code="VDI001").exists())

    def test_multiple_institutions_with_unique_codes(self):
        """
        The function tests creating multiple institutions with unique codes in a Python Django
        application.
        """
        inst1 = Institution.objects.create(
            name="Institute One",
            code="INST1"
        )
        inst2 = Institution.objects.create(
            name="Institute Two",
            code="INST2"
        )
        self.assertNotEqual(inst1.code, inst2.code)
        self.assertEqual(Institution.objects.count(), 2)

    def test_institution_creation_with_duplicate_code(self):
        """
        The function tests creating an Institution with a duplicate code to ensure it raises an
        IntegrityError.
        """
        Institution.objects.create(
            name="Original Institute",
            code="DUPLICATE01"
        )
        with self.assertRaises(IntegrityError):
            Institution.objects.create(
                name="Duplicate Institute",
                code="DUPLICATE01"
            )

    def test_institution_creation_without_website(self):
        """
        The function creates an Institution object without a website and asserts that the website
        attribute is None.
        """
        institution = Institution.objects.create(
            name="Blank Website Institute",
            code="BWI001"
        )
        self.assertIsNone(institution.website)

    def test_institution_creation_with_long_name(self):
        """
        The function tests the creation of an Institution object with a name that exceeds the maximum
        length allowed.
        """
        long_name = "B" * 256  # max_length is 255
        with self.assertRaises(DataError):
            Institution.objects.create(
                name=long_name,
                code="LONGNAME02"
            )

class ProgramModelTest(TestCase):
    def setUp(self):
        """
        The `setUp` function creates a new `Institution` object with specified name and code attributes.
        """
        self.institution = Institution.objects.create(
            name="Test Institution",
            code="TI001"
        )

    def test_program_accepts_positive_duration_years(self):
        """
        The function tests that the Program model accepts and stores positive integer values for duration_years.
        """
        program = Program.objects.create(
            institution=self.institution,
            name="Computer Science",
            duration_years=4
        )
        self.assertEqual(program.duration_years, 4)

    def test_program_associates_with_institution(self):
        """
        The function tests that the Program model associates correctly with an existing Institution.
        """
        program = Program.objects.create(
            institution=self.institution,
            name="Mathematics",
            duration_years=3
        )
        self.assertEqual(program.institution, self.institution)
        self.assertEqual(program.institution.name, "Test Institution")

    def test_program_name_field_persistence(self):
        """
        The function tests that the Program model saves and retrieves the name field accurately.
        """
        program = Program.objects.create(
            institution=self.institution,
            name="Physics",
            duration_years=2
        )
        retrieved = Program.objects.get(pk=program.pk)
        self.assertEqual(retrieved.name, "Physics")


    def test_program_name_exceeds_max_length(self):
        """
        The function tests that the Program model raises an error when the name exceeds the maximum length.
        """
        long_name = "A" * 256  # max_length is 255
        with self.assertRaises(DataError):
            Program.objects.create(
                institution=self.institution,
                name=long_name,
                duration_years=3
            )

    def test_program_deleted_on_institution_delete(self):
        """
        The function tests that deleting an Institution cascades and deletes associated Program instances.
        """
        program = Program.objects.create(
            institution=self.institution,
            name="Biology",
            duration_years=3
        )
        self.institution.delete()
        self.assertFalse(Program.objects.filter(pk=program.pk).exists())

    def test_program_str_representation(self):
        """
        The function tests that the Program model string representation returns formatted name and institution.
        """
        program = Program.objects.create(
            institution=self.institution,
            name="Engineering",
            duration_years=5
        )
        expected_str = "Engineering - Test Institution"
        self.assertEqual(str(program), expected_str)

    def test_program_institution_none_raises_error(self):
        """
        The function tests that the Program model raises an error when institution is set to None.
        """
        with self.assertRaises(IntegrityError):
            Program.objects.create(
                institution=None,
                name="History",
                duration_years=3
            )
            
    def test_duration_cannot_be_zero(self):
        """
        The function tests that the duration of a program cannot be zero.
        """
        program = Program(
            institution=self.institution,
            name="CS Degree",
            duration_years=0
        )
        with self.assertRaises(ValidationError):
            program.full_clean()


   