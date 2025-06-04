from rest_framework import serializers
from .models import Institution, Program, Course, Unit, Fee, ExamRegistration

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'

class ExamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        fields = '__all__'
        read_only_fields = ['student', 'registered_on']