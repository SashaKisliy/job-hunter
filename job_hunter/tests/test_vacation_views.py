from django.test import TestCase
from django.urls import reverse
from job_hunter.models import Vacation


class VacationViewTests(TestCase):

    def setUp(self):
        self.vacation = Vacation.objects.create(
            title="Test Vacation",
            salary=100000,
            experience="1_year",
            location="Test Location",
            type_work="remote",
            type_work_time="full_time",
            description="Test Description",
        )

    def test_vacation_list_view(self):
        response = self.client.get(reverse("job_hunter:vacancies-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vacation.title)

    def test_vacation_detail_view(self):
        response = self.client.get(
            reverse("job_hunter:vacancies-detail",
                    kwargs={"pk": self.vacation.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vacation.title)
