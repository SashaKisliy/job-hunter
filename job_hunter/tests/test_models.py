from django.test import TestCase
from django.contrib.auth import get_user_model
from job_hunter.models import Category, Resume, Candidate, Vacation

User = get_user_model()


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category1")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Category1")
        self.assertEqual(str(self.category), "Category1")


class CandidateModelTest(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="First",
            last_name="Last",
            email="test@example.com",
        )

    def test_candidate_creation(self):
        self.assertEqual(self.candidate.username, "testuser")
        self.assertEqual(self.candidate.first_name, "First")
        self.assertEqual(self.candidate.last_name, "Last")
        self.assertEqual(self.candidate.email, "test@example.com")
        self.assertEqual(str(self.candidate), "First Last")


class ResumeModelTest(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="First",
            last_name="Last",
            email="test@example.com",
        )
        self.category = Category.objects.create(name="Category1")
        self.resume = Resume.objects.create(
            title="Resume Title",
            first_name="First",
            last_name="Last",
            email="test@example.com",
            phone="1234567890",
            location="Test Location",
            education="Test Education",
            experience="1_year",
            candidate=self.candidate,
        )
        self.resume.categories.add(self.category)

    def test_resume_creation(self):
        self.assertEqual(self.resume.title, "Resume Title")
        self.assertEqual(self.resume.first_name, "First")
        self.assertEqual(self.resume.last_name, "Last")
        self.assertEqual(self.resume.email, "test@example.com")
        self.assertEqual(self.resume.phone, "1234567890")
        self.assertEqual(self.resume.location, "Test Location")
        self.assertEqual(self.resume.education, "Test Education")
        self.assertEqual(self.resume.experience, "1_year")
        self.assertEqual(self.resume.candidate, self.candidate)
        self.assertIn(self.category, self.resume.categories.all())
        self.assertEqual(str(self.resume), "Resume Title (First Last)")


class VacationModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category1")
        self.candidate = Candidate.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="First",
            last_name="Last",
            email="test@example.com",
        )
        self.vacation = Vacation.objects.create(
            title="Vacation Title",
            salary=100000,
            experience="1_year",
            location="Test Location",
            type_work="remote",
            type_work_time="full_time",
            description="Test Description",
        )
        self.vacation.categories.add(self.category)
        self.vacation.candidates.add(self.candidate)

    def test_vacation_creation(self):
        self.assertEqual(self.vacation.title, "Vacation Title")
        self.assertEqual(self.vacation.salary, 100000)
        self.assertEqual(self.vacation.experience, "1_year")
        self.assertEqual(self.vacation.location, "Test Location")
        self.assertEqual(self.vacation.type_work, "remote")
        self.assertEqual(self.vacation.type_work_time, "full_time")
        self.assertEqual(self.vacation.description, "Test Description")
        self.assertIn(self.category, self.vacation.categories.all())
        self.assertIn(self.candidate, self.vacation.candidates.all())
        self.assertEqual(str(self.vacation), "Vacation Title (100000)")
