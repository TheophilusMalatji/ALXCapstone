from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sector, Career, Introduction, Education, Skill, Responsibility, Specialization, Roadmap
from .serializers import SectorSerializer, CareerSerializer, IntroductionSerializer,  EducationSerializer, SkillSerializer, ResponsibilitySerializer,  SpecializationSerializer, RoadmapSerializer



class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all().order_by("name")
    serializer_class = SectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all().select_related("sector")
    serializer_class = CareerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["sector__id"]
    search_fields = ["name", "overview"]


class IntroductionViewSet(viewsets.ModelViewSet):
    queryset = Introduction.objects.select_related("career")
    serializer_class = IntroductionSerializer


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
    queryset = Roadmap.objects.select_related("career").prefetch_related("education", "skills", "specializations")
    serializer_class = RoadmapSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["career__id"]
