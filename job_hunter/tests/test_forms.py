from django.test import TestCase
from django.contrib.auth import get_user_model
from job_hunter.forms import (
    CandidateRegistrationForm,
    ResumeForm,
    VacationForm,
    VacationSearchForm,
    SearchForm,
)
from job_hunter.models import Candidate, Resume, Vacation, Category

User = get_user_model()


class CandidateRegistrationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "SuperSecretPassword123",
            "password2": "SuperSecretPassword123",
        }
        form = CandidateRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "SuperSecretPassword123",
            "password2": "DifferentPassword123",
        }
        form = CandidateRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class ResumeFormTest(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create_user(
            username="testuser", password="testpass"
        )

    def test_valid_form(self):
        category = Category.objects.create(name="Category1")
        form_data = {
            "title": "Resume Title",
            "first_name": "First",
            "last_name": "Last",
            "email": "test@example.com",
            "phone": "1234567890",
            "location": "Test Location",
            "education": "Test Education",
            "experience": "1_year",
            "categories": [category.pk],
        }
        form = ResumeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {}
        form = ResumeForm(data=form_data)
        self.assertFalse(form.is_valid())


class VacationFormTest(TestCase):
    def test_valid_form(self):
        category = Category.objects.create(name="Category1")
        form_data = {
            "title": "Vacation Title",
            "salary": 100000,
            "experience": "1_year",
            "location": "Test Location",
            "type_work": "remote",
            "type_work_time": "full_time",
            "description": "Test Description",
            "categories": [category.pk],
        }
        form = VacationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {}
        form = VacationForm(data=form_data)
        self.assertFalse(form.is_valid())


class VacationSearchFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "title": "Vacation Title",
            "experience": "1_year",
            "location": "Test Location",
            "type_work": "remote",
            "type_work_time": "full_time",
            "min_salary": 50000,
            "max_salary": 150000,
        }
        form = VacationSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form_data = {}
        form = VacationSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class SearchFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "query": "test query",
            "location": "test location",
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form_data = {}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
