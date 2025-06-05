from rest_framework import serializers
from .models import CareerAssessment, CareerRecommendation

# The `CareerAssessmentSerializer` class is a Django REST framework serializer for the
# `CareerAssessment` model with all fields included.
class CareerAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerAssessment
        fields = '__all__'

# The `CareerRecommendationSerializer` class is a Django REST framework serializer for the
# `CareerRecommendation` model with all fields included.
class CareerRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerRecommendation
        fields = '__all__'
