from rest_framework import serializers
from .models import Institution, Program, Course, Unit, Fee

# The `InstitutionSerializer` class is a Django REST framework serializer for the `Institution` model
# that includes all fields.
class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


# The `ProgramSerializer` class is a Django REST framework serializer for the `Program` model that
# includes all fields.
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


# The `CourseSerializer` class is a Django REST framework serializer for the `Course` model with all
# fields included.
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


# The `UnitSerializer` class is a Django REST framework serializer for the `Unit` model with all
# fields included.
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


# The `FeeSerializer` class is a Django REST framework serializer for the `Fee` model with all fields
# included.
class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'

