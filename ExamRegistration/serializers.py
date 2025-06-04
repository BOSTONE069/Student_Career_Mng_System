from rest_framework import serializers
from .models import ExamRegistration

class ExamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        fields = '__all__'
        read_only_fields = ['student', 'registered_on']