from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Guide, Payer
from .serializers import GuideSerializer, PayerNameSerializer
from .filters import GuideFilter

class GuideViewSet(viewsets.ModelViewSet):
    serializer_class = GuideSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GuideFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Guide.objects.select_related(
                'patient', 'clinic', 'payer', 'guide_type', 'status'
            ).all()

        user_clinics = user.clinics.all()
        return Guide.objects.filter(clinic__in=user_clinics).select_related(
            'patient', 'clinic', 'payer', 'guide_type', 'status'
        )

class PayerViewSet(viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer
    permission_classes = [IsAuthenticated]
sses = [IsAuthenticated]
