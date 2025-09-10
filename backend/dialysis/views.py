from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from rest_framework import serializers
from .models import Patient, PatientHistory, ExitType
from .serializers import PatientSerializer, PatientHistorySerializer, ExitTypeSerializer
from documents.models import Document, DocumentType
from organization.models import Clinic

class ExitTypeViewSet(viewsets.ModelViewSet):
    queryset = ExitType.objects.all()
    serializer_class = ExitTypeSerializer
    permission_classes = [IsAdminUser]

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        clinic_id = self.request.query_params.get('clinic', None)

        if user.is_superuser:
            queryset = Patient.objects.filter(is_active=True)
            if clinic_id:
                return queryset.filter(clinic_id=clinic_id).select_related('clinic')
            return queryset.select_related('clinic')

        user_clinics = user.clinics.all()
        if not clinic_id:
            return Patient.objects.none()

        try:
            requested_clinic = user_clinics.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Patient.objects.none()

        return Patient.objects.filter(
            clinic=requested_clinic,
            is_active=True
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

        mandatory_docs = clinic.mandatory_document_types.filter(category=DocumentType.Category.PATIENT)
        errors = {}
        for doc_type in mandatory_docs:
            if f'files[{doc_type.id}]' not in request.FILES:
                errors[doc_type.name] = f"Documento '{doc_type.name}' é obrigatório."
        
        if errors:
            return Response({"mandatory_documents": errors}, status=status.HTTP_400_BAD_REQUEST)

        patient_serializer = self.get_serializer(data=request.data)
        patient_serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                patient = patient_serializer.save()

                for key, uploaded_file in request.FILES.items():
                    if key.startswith('files[') and key.endswith(']'):
                        doc_type_id = key[6:-1]
                        try:
                            doc_type = DocumentType.objects.get(id=doc_type_id)
                            Document.objects.create(
                                clinic=clinic,
                                content_object=patient,
                                type=doc_type,
                                file=uploaded_file,
                                created_by=request.user
                            )
                        except DocumentType.DoesNotExist:
                            pass
            
            headers = self.get_success_headers(patient_serializer.data)
            return Response(patient_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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