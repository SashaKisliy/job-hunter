from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Candidate, Category, Resume, Vacation


@admin.register(Candidate)
class CandidateAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("display_resumes",
                                             "display_favorites")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("favorites",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "favorites",
                    )
                },
            ),
        )
    )

    def display_resumes(self, obj):
        return format_html(
            ", ".join([resume.title for resume in obj.resumes.all()])
        )

    display_resumes.short_description = "Resumes"

    def display_favorites(self, obj):
        return format_html(
            ", ".join([vacation.title for vacation in obj.favorites.all()])
        )

    display_favorites.short_description = "Favorites"


admin.site.register(Category)
admin.site.register(Resume)
admin.site.register(Vacation)
