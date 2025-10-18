from rest_framework.routers import DefaultRouter
from .views import (
    SectorViewSet,
    CareerViewSet,
    IntroductionViewSet,
    EducationViewSet,
    SkillViewSet,
    ResponsibilityViewSet,
    SpecializationViewSet,
    RoadmapViewSet,
    CareerDetailViewSet # New ViewSet
)

router = DefaultRouter()

# Core Endpoints
router.register(r'sectors', SectorViewSet)
router.register(r'careers', CareerViewSet) # Use this for list and single detailed retrieval
router.register(r'career-details', CareerDetailViewSet, basename='career-detail') # Alternative detailed endpoint

# Individual/Auxiliary Endpoints (less common frontend calls now)
router.register(r'introductions', IntroductionViewSet)
router.register(r'education', EducationViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'responsibilities', ResponsibilityViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'roadmaps', RoadmapViewSet)

urlpatterns = router.urls
