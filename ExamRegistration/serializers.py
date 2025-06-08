from rest_framework import serializers
from .models import ExamRegistration

# The `ExamRegistrationSerializer` class is a Django REST framework serializer for the
# `ExamRegistration` model with specified read-only fields.
class ExamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        fields = '__all__'
        read_only_fields = ['student', 'registered_on']