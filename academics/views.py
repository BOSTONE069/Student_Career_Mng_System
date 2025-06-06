from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework import viewsets
from .models import Institution, Program, Course, Unit
from .serializers import InstitutionSerializer, ProgramSerializer, CourseSerializer, UnitSerializer

# This class defines a view set for handling CRUD operations on Institution objects using a specified
# serializer.
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


# This class defines a view set for the Program model with a specified queryset and serializer class.
class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


# This class defines a view set for the Course model in Django, with a queryset that retrieves all
# Course objects and a serializer class for Course objects.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# This class represents a view set for the Unit model in Django, with a queryset of all Unit objects
# and using the UnitSerializer for serialization.
class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

