

# Register your models here.
from django.contrib import admin
from .models import (
    Sector,
    Career,
    Introduction,
    Education,
    Skill,
    Responsibility,
    Specialization,
    Roadmap,
)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name", "description")


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("name", "sector", "average_salary", "created_at")
    list_filter = ("sector",)
    search_fields = ("name", "overview", "job_outlook")
    autocomplete_fields = ("sector",)
    ordering = ("name",)


@admin.register(Introduction)
class IntroductionAdmin(admin.ModelAdmin):
    list_display = ("career", "created_at")
    search_fields = ("career__name", "content")
    autocomplete_fields = ("career",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("name", "nqf_level", "duration_years", "created_at")
    search_fields = ("name", "description")
    list_filter = ("nqf_level",)
    ordering = ("name",)
    filter_horizontal = ("careers",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)
    filter_horizontal = ("careers",)


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ("career", "short_description", "created_at")
    search_fields = ("career__name", "description")
    autocomplete_fields = ("career",)

    def short_description(self, obj):
        return (obj.description[:75] + "...") if len(obj.description) > 75 else obj.description
    short_description.short_description = "Description"


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name", "career", "created_at")
    search_fields = ("name", "career__name", "description")
    autocomplete_fields = ("career",)
    ordering = ("career", "name")


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("career", "created_at")
    search_fields = ("career__name", "description")
    autocomplete_fields = ("career",)
    filter_horizontal = ("education", "skills", "specializations")