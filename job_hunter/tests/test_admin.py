from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.urls import reverse
from job_hunter.models import Candidate, Category, Resume, Vacation
from job_hunter.admin import CandidateAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminSiteTestCase(TestCase):
    def setUp(self):
        # Create a superuser for accessing the admin site
        self.admin_user = User.objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.client.force_login(self.admin_user)

        # Create sample data for testing
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
        self.candidate.favorites.add(self.vacation)

    def test_candidate_admin_display_resumes(self):
        candidate_admin = CandidateAdmin(Candidate, AdminSite())
        self.assertEqual(
            candidate_admin.display_resumes(self.candidate), "Resume Title"
        )

    def test_candidate_admin_display_favorites(self):
        candidate_admin = CandidateAdmin(Candidate, AdminSite())
        self.assertEqual(
            candidate_admin.display_favorites(self.candidate), "Vacation Title"
        )

    def test_admin_candidate_list_view(self):
        url = reverse("admin:job_hunter_candidate_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertContains(response, "Vacation Title")

    def test_admin_candidate_change_view(self):
        url = reverse("admin:job_hunter_candidate_change",
                      args=[self.candidate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")
        self.assertContains(response, "Vacation Title")

    def test_admin_category_list_view(self):
        url = reverse("admin:job_hunter_category_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Category1")

    def test_admin_resume_list_view(self):
        url = reverse("admin:job_hunter_resume_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resume Title")

    def test_admin_vacation_list_view(self):
        url = reverse("admin:job_hunter_vacation_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vacation Title")
