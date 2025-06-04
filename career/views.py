from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import CareerAssessment, CareerRecommendation
from .serializers import CareerAssessmentSerializer, CareerRecommendationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import openai
from django.conf import settings


class CareerAssessmentView(generics.CreateAPIView):
    queryset = CareerAssessment.objects.all()
    serializer_class = CareerAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(student=self.request.user)
        # Generate recommendation
        recommendation = generate_recommendation(instance)
        CareerRecommendation.objects.create(
            student=self.request.user,
            recommendation_text=recommendation
        )

def generate_recommendation(assessment):
    import openai

def generate_recommendation(assessment):
    prompt = f"""
You are a career advisor. A student has submitted the following:
- Interests: {assessment.interests}
- Skills: {assessment.skills}
- Academic strengths: {assessment.academic_strengths}

Suggest 3 suitable career paths for the student. Include a brief explanation for each career, tailored to the given information.
"""

    openai.api_key = settings.OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful career guidance assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message['content']

    except Exception as e:
        return "An error occurred while generating the recommendation. Please try again later."


class CareerRecommendationView(generics.ListAPIView):
    serializer_class = CareerRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CareerRecommendation.objects.filter(student=self.request.user)
