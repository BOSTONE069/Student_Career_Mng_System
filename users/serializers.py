from rest_framework import serializers
from .models import Student
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = Student
        fields = ('username', 'email', 'student_id', 'password')

    def create(self, validated_data):
        user = Student.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            student_id=validated_data['student_id']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
