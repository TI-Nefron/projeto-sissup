from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated] # <-- Garante que só usuários logados acessem

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Patient.objects.filter(is_active=True).select_related('clinic')

        user_clinics = user.clinics.all()
        return Patient.objects.filter(
            clinic__in=user_clinics, 
            is_active=True
        ).select_related('clinic')