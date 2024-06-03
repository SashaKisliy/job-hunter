from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Resume(models.Model):
    class ExperienceChoices(models.TextChoices):
        NO_EXPERIENCE = "no_experience", "No experience"
        ONE_YEAR = "1_year", "1 year"
        THREE_YEARS = "3_years", "3 years"
        FIVE_YEARS = "5_years", "5 years"

    title = models.CharField(
        max_length=255
    )
    first_name = models.CharField(
        max_length=255
    )
    last_name = models.CharField(
        max_length=255
    )
    email = models.EmailField()
    phone = models.CharField(
        max_length=20
    )
    location = models.CharField(
        max_length=255
    )
    education = models.CharField(
        max_length=255
    )
    experience = models.CharField(
        max_length=20,
        choices=ExperienceChoices.choices
    )
    categories = models.ManyToManyField(
        Category,
        related_name="resumes"
    )
    candidate = models.ForeignKey(
        'Candidate',
        related_name='resumes',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.first_name} {self.last_name})"


class Candidate(AbstractUser):
    favorites = models.ManyToManyField(
        "Vacation",
        related_name="favorited_by",
        blank=True
    )

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("job_hunter:candidates-detail", kwargs={"pk": self.pk})


class Vacation(models.Model):
    class ExperienceChoices(models.TextChoices):
        NO_EXPERIENCE = "no_experience", "No experience"
        ONE_YEAR = "1_year", "1 year"
        THREE_YEARS = "3_years", "3 years"
        FIVE_YEARS = "5_years", "5 years"

    class TypeWorkChoices(models.TextChoices):
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        OFFICE = "office", "Office"

    class TypeWorkTimeChoices(models.TextChoices):
        PART_TIME = "part_time", "Part time"
        FULL_TIME = "full_time", "Full time"

    title = models.CharField(
        max_length=255
    )
    salary = models.BigIntegerField()
    experience = models.CharField(
        max_length=20,
        choices=ExperienceChoices.choices
    )
    location = models.CharField(
        max_length=255
    )
    type_work = models.CharField(
        max_length=20,
        choices=TypeWorkChoices.choices
    )
    type_work_time = models.CharField(
        max_length=20,
        choices=TypeWorkTimeChoices.choices
    )
    description = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    categories = models.ManyToManyField(
        Category,
        related_name="vacations"
    )
    candidates = models.ManyToManyField(
        Candidate,
        related_name="vacations",
        blank=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.title} ({self.salary})"
