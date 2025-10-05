from rest_framework import serializers
from .models import Sector, Career, Introduction, Education, Skill, Responsibility, Specialization, Roadmap



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


class CareerSerializer(serializers.ModelSerializer):
    sector = SectorSerializer(read_only=True)
    sector_id = serializers.PrimaryKeyRelatedField(
        source='sector', queryset=Sector.objects.all(), write_only=True
    )

    skills = SkillSerializer(many=True, read_only=True)
    education_options = EducationSerializer(many=True, read_only=True)
    responsibilities = ResponsibilitySerializer(many=True, read_only=True)
    specializations = SpecializationSerializer(many=True, read_only=True)

    class Meta:
        model = Career
        fields = [
            'id', 'name', 'sector', 'sector_id', 'overview', 'average_salary',
            'job_outlook', 'skills', 'education_options', 'responsibilities', 'specializations'
        ]


class IntroductionSerializer(serializers.ModelSerializer):
    career = CareerSerializer(read_only=True)
    career_id = serializers.PrimaryKeyRelatedField(
        source='career', queryset=Career.objects.all(), write_only=True
    )

    class Meta:
        model = Introduction
        fields = ['id', 'career', 'career_id', 'content']


class RoadmapSerializer(serializers.ModelSerializer):
    career = CareerSerializer(read_only=True)
    career_id = serializers.PrimaryKeyRelatedField(
        source='career', queryset=Career.objects.all(), write_only=True
    )

    education = EducationSerializer(many=True, read_only=True)
    education_ids = serializers.PrimaryKeyRelatedField(
        source='education', many=True, queryset=Education.objects.all(), write_only=True
    )

    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        source='skills', many=True, queryset=Skill.objects.all(), write_only=True
    )

    specializations = SpecializationSerializer(many=True, read_only=True)
    specialization_ids = serializers.PrimaryKeyRelatedField(
        source='specializations', many=True, queryset=Specialization.objects.all(), write_only=True
    )

    class Meta:
        model = Roadmap
        fields = [
            'id', 'career', 'career_id', 'description',
            'education', 'education_ids', 'skills', 'skill_ids',
            'specializations', 'specialization_ids'
        ]
