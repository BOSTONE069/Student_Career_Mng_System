from django.shortcuts import render
from rest_framework import generics
from .models import CareerAssessment, CareerRecommendation
from .serializers import CareerAssessmentSerializer, CareerRecommendationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from openai import AzureOpenAI
import os
import logging  # For better error handling/logging

# Set up logger
logger = logging.getLogger(__name__)

# Initialize Azure OpenAI client
try:
    client = AzureOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_version="2024-02-15-preview",
        api_key=settings.AZURE_OPENAI_KEY
    )
except Exception as e:
    logger.error("Failed to initialize AzureOpenAI client: %s", e)
    raise

class CareerAssessmentView(generics.CreateAPIView):
    queryset = CareerAssessment.objects.all()
    serializer_class = CareerAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(student=self.request.user)
        recommendation = generate_recommendation(instance)

        if recommendation:
            CareerRecommendation.objects.create(
                student=self.request.user,
                recommendation_text=recommendation
            )
        else:
            CareerRecommendation.objects.create(
                student=self.request.user,
                recommendation_text="Could not generate recommendation at this time."
            )

def generate_recommendation(assessment):
    prompt = f"""
You are a career advisor. A student has submitted the following:
- Interests: {assessment.interests}
- Skills: {assessment.skills}
- Academic strengths: {assessment.academic_strengths}

Suggest 3 suitable career paths for the student. Include a brief explanation for each career, tailored to the given information.
"""

    try:
        response = client.chat.completions.create(
            model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,  # e.g., "gpt-4o"
            messages=[
                {"role": "system", "content": "You are a helpful career guidance assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error("Azure OpenAI API error: %s", e)
        return None

class CareerRecommendationView(generics.ListAPIView):
    serializer_class = CareerRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CareerRecommendation.objects.filter(student=self.request.user)