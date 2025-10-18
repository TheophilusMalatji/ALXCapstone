from rest_framework import serializers
from .models import (
    Sector, Career, Introduction, Education, Skill, Responsibility, 
    Specialization, Certification, Roadmap, Phase
)

# --- Base Model Serializers ---

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'
        
class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

# --- Nested Serializers for Roadmap Phases ---

class PhaseSerializer(serializers.ModelSerializer):
    """Serializes a single Phase, including its related education, skills, and certifications."""
    required_education = EducationSerializer(many=True, read_only=True)
    required_skills = SkillSerializer(many=True, read_only=True)
    required_specializations = SpecializationSerializer(many=True, read_only=True)
    required_certifications = CertificationSerializer(many=True, read_only=True)

    class Meta:
        model = Phase
        fields = [
            'id', 'name', 'order', 'description', 
            'required_education', 'required_skills', 
            'required_specializations', 'required_certifications'
        ]

# --- Aggregating Serializers ---

class RoadmapSerializer(serializers.ModelSerializer):
    """Roadmap serializer including nested Phases for full progression details."""
    # Note: Removed M2M fields from the Roadmap model itself, as progression logic moved to Phase
    phases = PhaseSerializer(many=True, read_only=True)

    class Meta:
        model = Roadmap
        fields = [
            'id', 'career', 'description', 'phases'
        ]
        # Temporarily excluding write-only fields for M2M until they are updated or removed
        read_only_fields = ['career']





class IntroductionSerializer(serializers.ModelSerializer):
    """Detailed Introduction serializer."""
    class Meta:
        model = Introduction
        fields = ['career', 'id', 'content', 'education_duration_years', 'education_duration_months']

class CareerSerializer(serializers.ModelSerializer):
    sector = SectorSerializer(read_only=True)
    sector_id = serializers.PrimaryKeyRelatedField(
    source='sector', queryset=Sector.objects.all(), write_only=True
    )
    
    # FIX: Include the nested IntroductionSerializer here
    

    skills = SkillSerializer(many=True, read_only=True)
    education_options = EducationSerializer(many=True, read_only=True)
    responsibilities = ResponsibilitySerializer(many=True, read_only=True)
    specializations = SpecializationSerializer(many=True, read_only=True)
    introduction = IntroductionSerializer(read_only=True)
    class Meta:
        model = Career
        fields = [
            'id', 'name', 'sector', 'sector_id', 'overview', 'average_salary', 
            'job_outlook', 
            'introduction', # <-- Added nested introduction field
            'skills', 'education_options', 'responsibilities', 'specializations'
        ]


class CareerDetailSerializer(serializers.ModelSerializer):
    """
    MASTER SERIALIZER: Aggregates all career-related details into a single JSON object.
    This fulfills the requirement of minimizing front-end API calls.
    """
    sector = SectorSerializer(read_only=True)
    introduction = IntroductionSerializer(read_only=True)
    responsibilities = ResponsibilitySerializer(many=True, read_only=True)
    specializations = SpecializationSerializer(many=True, read_only=True)
    roadmap = RoadmapSerializer(read_only=True)
    
    # Simple list of all unique skills/education for the entire career (denormalized from phases for easy access)
    all_skills = SkillSerializer(many=True, read_only=True, source='skills')
    all_education = EducationSerializer(many=True, read_only=True, source='education_options')

    class Meta:
        model = Career
        fields = [
            'id', 'name', 'sector', 'overview', 'average_salary', 'job_outlook',
            'introduction', 'responsibilities', 'specializations', 'roadmap',
            'all_skills', 'all_education'
        ]
