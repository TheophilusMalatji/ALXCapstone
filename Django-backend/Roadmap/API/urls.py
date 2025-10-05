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
)

router = DefaultRouter()

router.register(r'sectors', SectorViewSet)
router.register(r'careers', CareerViewSet)
router.register(r'introductions', IntroductionViewSet)
router.register(r'education', EducationViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'responsibilities', ResponsibilityViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'roadmaps', RoadmapViewSet)

urlpatterns = router.urls