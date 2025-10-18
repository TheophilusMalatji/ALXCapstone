from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Sector, Career, Introduction, Education, Skill, Responsibility, 
    Specialization, Roadmap, Phase, Certification
)
from .serializers import (
    SectorSerializer, CareerSerializer, IntroductionSerializer,  
    EducationSerializer, SkillSerializer, ResponsibilitySerializer,  
    SpecializationSerializer, RoadmapSerializer, CertificationSerializer,
    PhaseSerializer, CareerDetailSerializer
)


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all().order_by("name")
    serializer_class = SectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class CareerViewSet(viewsets.ModelViewSet):
    """
    View for the list of careers. Optimized for quick listing.
    """
    queryset = Career.objects.all().select_related("sector")
    serializer_class = CareerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["sector__id"]
    search_fields = ["name", "overview"]
    
    # Overriding retrieve to use the detailed serializer for single lookup
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CareerDetailSerializer(instance)
        return Response(serializer.data)


class CareerDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    NEW VIEWSET: Provides a single, optimized endpoint for all career details.
    The primary purpose is to use the heavy prefetching.
    """
    queryset = Career.objects.all().select_related(
        'sector', 'introduction', 'roadmap'
    ).prefetch_related(
        'responsibilities', 
        'specializations', 
        'skills', # M2M for the whole career
        'education_options', # M2M for the whole career
        
        # Deep prefetch for the Roadmap phases and their M2M fields
        'roadmap__phases__required_education',
        'roadmap__phases__required_skills',
        'roadmap__phases__required_specializations',
        'roadmap__phases__required_certifications',
    ).order_by("name")
    serializer_class = CareerDetailSerializer
    
    # We only want the detail view, so we make it ReadOnly and allow lookup by ID
    lookup_field = 'id'
    
    # Custom action to provide a single, easy-to-call endpoint (e.g., /api/careers/detailed/)
    # Note: For simplicity, I've integrated this functionality into the standard CareerViewSet retrieve method above. 
    # If you need a separate list view for *all* detailed careers, you can use this viewset's list method.


class IntroductionViewSet(viewsets.ModelViewSet):
    queryset = Introduction.objects.select_related("career")
    serializer_class = IntroductionSerializer
    # Only expose filtering by career
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["career__id"]


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all().order_by("name")
    serializer_class = EducationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class ResponsibilityViewSet(viewsets.ModelViewSet):
    queryset = Responsibility.objects.select_related("career")
    serializer_class = ResponsibilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["career__id"]


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.select_related("career")
    serializer_class = SpecializationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["career__id"]


class RoadmapViewSet(viewsets.ModelViewSet):
    """
    This view is now less critical as the CareerDetailViewSet is the main endpoint,
    but it is kept for managing Roadmaps individually.
    """
    queryset = Roadmap.objects.select_related("career").prefetch_related("phases")
    serializer_class = RoadmapSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["career__id"]
