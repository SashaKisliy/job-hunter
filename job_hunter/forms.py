from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Candidate, Resume, Vacation


class CandidateRegistrationForm(UserCreationForm):
    class Meta:
        model = Candidate
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ['candidate']


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = "__all__"


class VacationSearchForm(forms.Form):
    title = forms.CharField(max_length=255, required=False, label="Title")
    experience = forms.ChoiceField(
        choices=[("", "Any")] + Vacation.ExperienceChoices.choices,
        required=False,
        label="Experience",
    )
    location = forms.CharField(
        max_length=255,
        required=False,
        label="Location"
    )
    type_work = forms.ChoiceField(
        choices=[("", "Any")] + Vacation.TypeWorkChoices.choices,
        required=False,
        label="Type of Work",
    )
    type_work_time = forms.ChoiceField(
        choices=[("", "Any")] + Vacation.TypeWorkTimeChoices.choices,
        required=False,
        label="Type of Work Time",
    )
    min_salary = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, label="Min Salary"
    )
    max_salary = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, label="Max Salary"
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Print your request", "class": "form-control"
            }
        ),
        required=False,
    )
    location = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Print a location", "class": "form-control"}
        ),
    )
