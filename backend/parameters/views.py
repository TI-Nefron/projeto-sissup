from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import GuideType, ProcedureStatus
from .serializers import GuideTypeSerializer, ProcedureStatusSerializer

class GuideTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuideType.objects.filter(is_active=True)
    serializer_class = GuideTypeSerializer
    permission_classes = [IsAuthenticated]

class ProcedureStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProcedureStatus.objects.filter(is_active=True)
    serializer_class = ProcedureStatusSerializer
    permission_classes = [IsAuthenticated]
