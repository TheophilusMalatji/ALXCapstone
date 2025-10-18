from django.db import models
import uuid

class TimestampedModel(models.Model):
    """Abstract model that adds created and updated timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Sector(TimestampedModel):
    """High-level grouping of related careers (e.g., IT, Finance, Healthcare)."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Career(TimestampedModel):
    """Represents a specific career or occupation."""
    name = models.CharField(max_length=255, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="careers")
    overview = models.TextField(blank=True, null=True)  # Short summary
    average_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_outlook = models.TextField(blank=True, null=True)  # Optional (e.g. future growth, demand)

    def __str__(self):
        return self.name


class Introduction(TimestampedModel):
    """Detailed explanation or introduction for a career."""
    career = models.OneToOneField(Career, on_delete=models.CASCADE, related_name="introduction")
    content = models.TextField()
    education_duration_years = models.IntegerField()
    education_duration_months = models.IntegerField()


    def __str__(self):
        return f"Introduction for {self.career.name}"


class Education(TimestampedModel):
    """Educational paths related to a career."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    nqf_level = models.IntegerField(blank=True, null=True)
    duration_years = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    careers = models.ManyToManyField(Career, related_name="education_options", blank=True)

    def __str__(self):
        return self.name


class Skill(TimestampedModel):
    """Skills required or recommended for a career."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    careers = models.ManyToManyField(Career, related_name="skills", blank=True)

    def __str__(self):
        return self.name


class Responsibility(TimestampedModel):
    """Expected duties or job responsibilities for a given career."""
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="responsibilities")
    description = models.TextField()

    def __str__(self):
        return f"Responsibility for {self.career.name}"


class Specialization(TimestampedModel):
    """Specialized areas within a broader career (e.g., software engineer → frontend/backend)."""
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="specializations")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.career.name})"
    
class Certification(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True)


class Roadmap(TimestampedModel):
    """Defines a roadmap to reach a particular career."""
    career = models.OneToOneField(Career, on_delete=models.CASCADE, related_name="roadmap")
    description = models.TextField(blank=True, null=True)

    # Relationships
    education = models.ManyToManyField(Education, blank=True, related_name="roadmaps")
    skills = models.ManyToManyField(Skill, blank=True, related_name="roadmaps")
    specializations = models.ManyToManyField(Specialization, blank=True, related_name="roadmaps")

    def __str__(self):
        return f"Roadmap for {self.career.name}"
    

# In your models.py file

# ... (existing TimestampedModel, Career, Roadmap definitions) ...

class Phase(TimestampedModel):
    """
    Represents a named stage or step in a career roadmap,
    directly linking to the required skills and education for that step.
    """
    roadmap = models.ForeignKey(
        'Roadmap',
        on_delete=models.CASCADE,
        related_name="phases",
        help_text="The career roadmap this phase belongs to."
    )
    name = models.CharField(
        max_length=255,
        help_text="The title of the phase (e.g., 'Phase 1: Academic Base')."
    )
    order = models.PositiveIntegerField(
        help_text="The sequence in which the phase occurs in the roadmap."
    )
    description = models.TextField(blank=True,null=True,
        help_text="Detailed description of the goals/actions in this specific phase."
    )

    # Direct Many-to-Many relationships as requested
    required_education = models.ManyToManyField(
        'Education', 
        blank=True, 
        related_name='phases_required', 
        help_text="Educational paths specifically completed or started in this phase."
    )
    required_skills = models.ManyToManyField(
        'Skill', 
        blank=True, 
        related_name='phases_required', 
        help_text="Skills that must be acquired or mastered in this phase."
    )
    required_specializations = models.ManyToManyField(
        'Specialization', 
        blank=True, 
        related_name='phases_required', 
        help_text="Specializations that are typically achieved or started in this phase."
    )
    required_certifications = models.ManyToManyField(
        'Certification', 
        blank=True, 
        related_name='phases_required', 
        help_text="Professional certifications obtained in this phase."
    )

    class Meta:
        unique_together = ('roadmap', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.name} for {self.roadmap.career.name}"