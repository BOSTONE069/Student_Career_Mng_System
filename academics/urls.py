from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutionViewSet, ProgramViewSet, CourseViewSet, UnitViewSet

router = DefaultRouter()
router.register('institutions', InstitutionViewSet)
router.register('programs', ProgramViewSet)
router.register('courses', CourseViewSet)
router.register('units', UnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
