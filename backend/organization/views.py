from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.urls import reverse
from .models import Clinic
from .serializers import ClinicSerializer

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [IsAdminUser]

class ParameterizationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        return Response({
            'clinics': request.build_absolute_uri(reverse('organization:clinic-list')),
            'guide_types': request.build_absolute_uri(reverse('parameters:guidetype-list')),
            'procedure_statuses': request.build_absolute_uri(reverse('parameters:procedurestatus-list')),
            'exit_types': request.build_absolute_uri(reverse('dialysis:tipo-de-saida-list')),
            'payers': request.build_absolute_uri(reverse('billing:payer-list')),
        })
