from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.db.models import Count
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import (
    CandidateRegistrationForm, ResumeForm, VacationSearchForm, SearchForm
)

from .models import (
    Vacation, Candidate, Resume, Category
)


def register(request):
    if request.method == "POST":
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("job_hunter:index")
    else:
        form = CandidateRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def index(request):
    form = SearchForm()
    vacancy_count = Vacation.objects.count()
    return render(
        request,
        "job_hunter/index.html",
        {"form": form, "vacancy_count": vacancy_count}
    )


def search(request):
    form = SearchForm(request.GET)
    vacancies = Vacation.objects.all()
    if request.GET:
        if form.is_valid():
            query = form.cleaned_data["query"]
            location = form.cleaned_data["location"]
            if query:
                vacancies = vacancies.filter(title__icontains=query)
            if location:
                vacancies = vacancies.filter(location__icontains=location)
    return render(
        request,
        "job_hunter/search_results.html",
        {"form": form, "vacancies": vacancies},
    )


class CategoryListView(generic.ListView):
    model = Category
    template_name = "job_hunter/categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(vacancies_count=Count("vacations"))


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "job_hunter/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context["vacations"] = category.vacations.all()
        return context


class VacationListView(generic.ListView):
    model = Vacation
    paginate_by = 3
    template_name = "job_hunter/vacation_list.html"
    context_object_name = "vacation_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VacationSearchForm(self.request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            experience = form.cleaned_data.get("experience")
            min_salary = form.cleaned_data.get("min_salary")
            max_salary = form.cleaned_data.get("max_salary")
            type_work = form.cleaned_data.get("type_work")
            type_work_time = form.cleaned_data.get("type_work_time")

            if title:
                queryset = queryset.filter(title__icontains=title)
            if experience:
                queryset = queryset.filter(experience=experience)
            if min_salary:
                queryset = queryset.filter(salary__gte=min_salary)
            if max_salary:
                queryset = queryset.filter(salary__lte=max_salary)
            if type_work:
                queryset = queryset.filter(type_work=type_work)
            if type_work_time:
                queryset = queryset.filter(type_work_time=type_work_time)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = VacationSearchForm(self.request.GET)
        return context


class VacationDetailView(generic.DetailView):
    model = Vacation


class CandidateDetailView(generic.DetailView):
    model = Candidate


class ResumeListView(generic.ListView):
    model = Resume


class ResumeDetailView(generic.DetailView):
    model = Resume


class ResumeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = "job_hunter/resume_form.html"

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.candidate = self.request.user
        resume.save()
        form.save_m2m()
        return redirect("job_hunter:candidates-detail",
                        pk=self.request.user.pk)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("job_hunter:candidates-detail",
                            kwargs={"pk": self.request.user.pk})


class ResumeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = "job_hunter/resume_form.html"

    def get_success_url(self):
        return reverse("job_hunter:candidates-detail",
                       kwargs={"pk": self.request.user.pk})


class ResumeDeleteView(generic.DeleteView):
    model = Resume

    def get_success_url(self):
        return reverse_lazy(
            "job_hunter:candidates-detail", kwargs={"pk": self.request.user.pk}
        )


@login_required
def apply_for_vacation(request, pk):
    vacation = get_object_or_404(Vacation, pk=pk)
    candidate = request.user
    vacation.candidates.add(candidate)
    return redirect("job_hunter:vacancies-detail", pk=pk)


@login_required
def add_to_favorites(request, pk):
    vacation = get_object_or_404(Vacation, pk=pk)
    candidate = request.user
    candidate.favorites.add(vacation)
    return redirect("job_hunter:vacancies-detail", pk=pk)


@login_required
def remove_from_favorites(request, pk):
    vacation = get_object_or_404(Vacation, pk=pk)
    request.user.favorites.remove(vacation)
    return redirect("job_hunter:vacancies-detail", pk=pk)
