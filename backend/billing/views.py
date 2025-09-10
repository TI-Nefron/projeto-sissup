from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Guide, Payer
from .serializers import GuideSerializer, PayerSerializer
from .filters import GuideFilter
from organization.models import Clinic
from audit.mixins import AuditableViewSetMixin

class GuideViewSet(AuditableViewSetMixin, viewsets.ModelViewSet):
    serializer_class = GuideSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GuideFilter
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        clinic_id = self.request.query_params.get('clinic', None)

        if user.is_superuser:
            queryset = Guide.objects.select_related('patient', 'clinic', 'payer', 'guide_type', 'status').all()
            if clinic_id:
                return queryset.filter(clinic_id=clinic_id)
            return queryset

        user_clinics = user.clinics.all()
        if not clinic_id:
            return Guide.objects.filter(clinic__in=user_clinics).select_related(
                'patient', 'clinic', 'payer', 'guide_type', 'status'
            )

        try:
            requested_clinic = user_clinics.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Guide.objects.none()

        return Guide.objects.filter(clinic=requested_clinic).select_related(
            'patient', 'clinic', 'payer', 'guide_type', 'status'
        )

    def create(self, request, *args, **kwargs):
        clinic_id = request.data.get('clinic')
        if not clinic_id:
            return Response({"clinic": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({"clinic": "Invalid clinic."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_superuser and clinic not in request.user.clinics.all():
            return Response({"detail": "You do not have permission to create a guide in this clinic."}, status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

class PayerViewSet(AuditableViewSetMixin, viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer
    permission_classes = [IsAdminUser]

class ClinicPayerListView(ListAPIView):
    serializer_class = PayerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clinic_id = self.kwargs['clinic_id']
        return Payer.objects.filter(clinics__id=clinic_id)
