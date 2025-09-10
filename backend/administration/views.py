from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from organization.models import Clinic
from parameters.models import GuideType, ProcedureStatus
from dialysis.models import ExitType
from accounts.models import Role
from .serializers import (
    UserSerializer,
    ClinicSerializer,
    GuideTypeSerializer,
    ProcedureStatusSerializer,
    ExitTypeSerializer,
    RoleSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from documents.models import DocumentType

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

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]

class ClinicMandatoryDocumentsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, clinic_id):
        print(">>>>>>>>>>>>>>>>>> HIT ClinicMandatoryDocumentsView GET")
        try:
            clinic = Clinic.objects.get(pk=clinic_id)
            mandatory_docs_ids = clinic.mandatory_document_types.values_list('id', flat=True)
            return Response(mandatory_docs_ids)
        except Clinic.DoesNotExist:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, clinic_id):
        print(">>>>>>>>>>>>>>>>>> HIT ClinicMandatoryDocumentsView POST")
        try:
            clinic = Clinic.objects.get(pk=clinic_id)
            document_type_ids = request.data.get('document_type_ids', [])
            
            if not isinstance(document_type_ids, list):
                return Response({"error": "document_type_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

            valid_document_types = DocumentType.objects.filter(id__in=document_type_ids)
            if len(valid_document_types) != len(document_type_ids):
                return Response({"error": "One or more document type IDs are invalid"}, status=status.HTTP_400_BAD_REQUEST)

            clinic.mandatory_document_types.set(valid_document_types)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Clinic.DoesNotExist:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)
