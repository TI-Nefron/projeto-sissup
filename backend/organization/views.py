from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Clinic
from .serializers import ClinicSerializer

class ClinicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Clinic.objects.filter(is_active=True)
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated]
