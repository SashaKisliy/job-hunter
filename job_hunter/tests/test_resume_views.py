from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from job_hunter.models import Resume, Candidate

User = get_user_model()


class ResumeViewTests(TestCase):

    def setUp(self):
        self.candidate = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.resume = Resume.objects.create(
            title="Resume",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="1234567890",
            location="Test Location",
            education="Test Education",
            experience="1_year",
            candidate=self.candidate,
        )
        self.client.login(username="testuser", password="testpass")

    def test_resume_list_view(self):
        response = self.client.get(reverse("job_hunter:resume-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.resume.title)

    def test_resume_detail_view(self):
        response = self.client.get(
            reverse("job_hunter:resume-detail", kwargs={"pk": self.resume.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.resume.title)

    def test_resume_delete_view(self):
        response = self.client.post(
            reverse("job_hunter:resume-delete", kwargs={"pk": self.resume.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Resume.objects.filter(pk=self.resume.pk).exists())
