from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import GuideType, ProcedureStatus
from .serializers import GuideTypeSerializer, ProcedureStatusSerializer

class GuideTypeViewSet(viewsets.ModelViewSet):
    queryset = GuideType.objects.all()
    serializer_class = GuideTypeSerializer
    permission_classes = [IsAdminUser]

class ProcedureStatusViewSet(viewsets.ModelViewSet):
    queryset = ProcedureStatus.objects.all()
    serializer_class = ProcedureStatusSerializer
    permission_classes = [IsAdminUser]

class ClinicGuideTypeListView(ListAPIView):
    serializer_class = GuideTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clinic_id = self.kwargs['clinic_id']
        return GuideType.objects.filter(clinics__id=clinic_id)

class ClinicProcedureStatusListView(ListAPIView):
    serializer_class = ProcedureStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clinic_id = self.kwargs['clinic_id']
        return ProcedureStatus.objects.filter(clinics__id=clinic_id)