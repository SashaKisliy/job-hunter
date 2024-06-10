from django.test import TestCase
from django.urls import reverse
from job_hunter.models import Category, Vacation


class CategoryViewTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.vacation = Vacation.objects.create(
            title="Test Vacation",
            salary=100000,
            experience="1_year",
            location="Test Location",
            type_work="remote",
            type_work_time="full_time",
            description="Test Description",
        )
        self.vacation.categories.add(self.category)

    def test_category_list_view(self):
        response = self.client.get(reverse("job_hunter:categories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_category_detail_view(self):
        response = self.client.get(
            reverse("job_hunter:category_detail",
                    kwargs={"pk": self.category.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.vacation.title)
