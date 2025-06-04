# exams/urls.py

from rest_framework.routers import DefaultRouter
from .views import ExamRegistrationViewSet

router = DefaultRouter()
router.register('registrations', ExamRegistrationViewSet, basename='exam-registration')

urlpatterns = router.urls
