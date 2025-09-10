from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Guide, Payer
from .serializers import GuideSerializer, PayerSerializer, PayerNameSerializer
from .filters import GuideFilter

class GuideViewSet(viewsets.ModelViewSet):
    serializer_class = GuideSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GuideFilter

    def get_queryset(self):
        user = self.request.user
        clinic_id = self.request.query_params.get('clinic', None)

        # Superuser pode ver tudo, mas ainda pode filtrar por clínica se o param for passado
        if user.is_superuser:
            queryset = Guide.objects.select_related('patient', 'clinic', 'payer', 'guide_type', 'status').all()
            if clinic_id:
                return queryset.filter(clinic_id=clinic_id)
            return queryset

        # Usuário normal
        user_clinics = user.clinics.all()
        if not clinic_id:
            # Exigir que usuários normais sempre filtrem por uma clínica
            return Guide.objects.none()

        # Verificar se o usuário tem acesso à clínica solicitada
        try:
            requested_clinic = user_clinics.get(id=clinic_id)
        except Guide.DoesNotExist:
            return Guide.objects.none()

        return Guide.objects.filter(clinic=requested_clinic).select_related(
            'patient', 'clinic', 'payer', 'guide_type', 'status'
        )

class PayerViewSet(viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer
    permission_classes = [IsAdminUser]

class ClinicPayerListView(ListAPIView):
    serializer_class = PayerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clinic_id = self.kwargs['clinic_id']
        return Payer.objects.filter(clinics__id=clinic_id)
