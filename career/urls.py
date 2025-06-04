from django.urls import path
from .views import CareerAssessmentView, CareerRecommendationView

urlpatterns = [
    path('assess/', CareerAssessmentView.as_view(), name='career-assess'),
    path('recommendations/', CareerRecommendationView.as_view(), name='career-recommendations'),
]
