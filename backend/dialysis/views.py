from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Patient, PatientHistory, ExitType
from .serializers import PatientSerializer, PatientHistorySerializer, ExitTypeSerializer
from organization.models import Clinic
from audit.mixins import AuditableViewSetMixin

class ExitTypeViewSet(AuditableViewSetMixin, viewsets.ModelViewSet):
    queryset = ExitType.objects.all()
    serializer_class = ExitTypeSerializer
    permission_classes = [IsAdminUser]

class PatientViewSet(AuditableViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        clinic_id = self.request.query_params.get('clinic', None)

        if user.is_superuser:
            queryset = Patient.objects.all()
            if clinic_id:
                return queryset.filter(clinic_id=clinic_id).select_related('clinic')
            return queryset.select_related('clinic')

        user_clinics = user.clinics.all()
        if not clinic_id:
            # Se nenhum ID de clínica for fornecido, retorne pacientes de todas as clínicas do usuário
            return Patient.objects.filter(clinic__in=user_clinics).select_related('clinic')

        try:
            requested_clinic = user_clinics.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Patient.objects.none()

        return Patient.objects.filter(
            clinic=requested_clinic
        ).select_related('clinic')

    def create(self, request, *args, **kwargs):
        clinic_id = request.data.get('clinic_id')
        if not clinic_id:
            return Response({"clinic_id": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({"clinic_id": "Invalid clinic."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_superuser and clinic not in request.user.clinics.all():
            return Response({"detail": "You do not have permission to create a patient in this clinic."}, status=status.HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)

class PatientHistoryViewSet(AuditableViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PatientHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PatientHistory.objects.all()

        user_clinics = user.clinics.all()
        return PatientHistory.objects.filter(clinic__in=user_clinics)

class ClinicExitTypeListView(ListAPIView):
    serializer_class = ExitTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clinic_id = self.kwargs['clinic_id']
        return ExitType.objects.filter(clinics__id=clinic_id)