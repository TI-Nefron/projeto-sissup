from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Patient, PatientHistory, ExitType
from .serializers import PatientSerializer, PatientHistorySerializer, ExitTypeSerializer

class ExitTypeViewSet(viewsets.ModelViewSet):
    queryset = ExitType.objects.all()
    serializer_class = ExitTypeSerializer
    permission_classes = [IsAdminUser]

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated] # <-- Garante que só usuários logados acessem

    def get_queryset(self):
        user = self.request.user
        clinic_id = self.request.query_params.get('clinic', None)

        if user.is_superuser:
            queryset = Patient.objects.filter(is_active=True)
            if clinic_id:
                return queryset.filter(clinic_id=clinic_id).select_related('clinic')
            return queryset.select_related('clinic')

        # Usuário não-superuser
        user_clinics = user.clinics.all()
        if not clinic_id:
            # Se nenhum ID de clínica for fornecido, não retorna nada para usuários normais
            return Patient.objects.none()

        # Verifica se o ID da clínica solicitado pertence às clínicas do usuário
        try:
            requested_clinic = user_clinics.get(id=clinic_id)
        except Patient.DoesNotExist:
            return Patient.objects.none() # Retorna queryset vazio se não tiver acesso

        return Patient.objects.filter(
            clinic=requested_clinic,
            is_active=True
        ).select_related('clinic')

class PatientHistoryViewSet(viewsets.ModelViewSet):
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