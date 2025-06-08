# exams/views.py

from rest_framework import viewsets, permissions
from .models import ExamRegistration
from .serializers import ExamRegistrationSerializer

# This class defines a view set for exam registration with permissions for authenticated users and a
# method to save the student information when creating a new registration.
class ExamRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ExamRegistration.objects.all()
    serializer_class = ExamRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
