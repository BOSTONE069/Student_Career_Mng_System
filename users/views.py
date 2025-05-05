from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from .models import Student

class RegisterView(generics.CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
