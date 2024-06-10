from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from job_hunter.models import Candidate, Vacation

User = get_user_model()


class CandidateViewTests(TestCase):

    def setUp(self):
        self.candidate = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.vacation = Vacation.objects.create(
            title="Test Vacation",
            salary=100000,
            experience="1_year",
            location="Test Location",
            type_work="remote",
            type_work_time="full_time",
            description="Test Description",
        )
        self.client.login(username="testuser", password="testpass")

    def test_candidate_detail_view(self):
        response = self.client.get(
            reverse("job_hunter:candidates-detail",
                    kwargs={"pk": self.candidate.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.candidate.username)

    def test_apply_for_vacation_view(self):
        response = self.client.post(
            reverse("job_hunter:apply-for-vacation",
                    kwargs={"pk": self.vacation.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.vacation.candidates.filter(
            pk=self.candidate.pk).exists()
        )

    def test_add_to_favorites_view(self):
        response = self.client.post(
            reverse("job_hunter:add-to-favorites",
                    kwargs={"pk": self.vacation.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.candidate.favorites.filter(
            pk=self.vacation.pk).exists()
        )

    def test_remove_from_favorites_view(self):
        self.candidate.favorites.add(self.vacation)
        response = self.client.post(
            reverse("job_hunter:remove-from-favorites",
                    kwargs={"pk": self.vacation.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.candidate.favorites.filter(
            pk=self.vacation.pk).exists()
        )
