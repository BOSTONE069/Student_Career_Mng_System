# exams/views.py

from rest_framework import viewsets, permissions
from .models import ExamRegistration
from .serializers import ExamRegistrationSerializer

class ExamRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ExamRegistration.objects.all()
    serializer_class = ExamRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
