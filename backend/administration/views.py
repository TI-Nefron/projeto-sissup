from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from organization.models import Clinic
from parameters.models import GuideType, ProcedureStatus
from dialysis.models import ExitType
from .serializers import (
    UserSerializer,
    ClinicSerializer,
    GuideTypeSerializer,
    ProcedureStatusSerializer,
    ExitTypeSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAdminUser]

class GuideTypeViewSet(viewsets.ModelViewSet):
    queryset = GuideType.objects.all()
    serializer_class = GuideTypeSerializer
    permission_classes = [permissions.IsAdminUser]

class ProcedureStatusViewSet(viewsets.ModelViewSet):
    queryset = ProcedureStatus.objects.all()
    serializer_class = ProcedureStatusSerializer
    permission_classes = [permissions.IsAdminUser]

class ExitTypeViewSet(viewsets.ModelViewSet):
    queryset = ExitType.objects.all()
    serializer_class = ExitTypeSerializer
    permission_classes = [permissions.IsAdminUser]