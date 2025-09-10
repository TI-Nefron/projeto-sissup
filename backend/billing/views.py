from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from .models import Guide, Payer
from .serializers import GuideSerializer, PayerSerializer, PayerNameSerializer
from .filters import GuideFilter
from documents.models import Document, DocumentType
from organization.models import Clinic

class GuideViewSet(viewsets.ModelViewSet):
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
            return Guide.objects.none()

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

        mandatory_docs = clinic.mandatory_document_types.filter(category=DocumentType.Category.GUIDE)
        errors = {}
        for doc_type in mandatory_docs:
            if f'files[{doc_type.id}]' not in request.FILES:
                errors[doc_type.name] = f"Documento '{doc_type.name}' é obrigatório."
        
        if errors:
            return Response({"mandatory_documents": errors}, status=status.HTTP_400_BAD_REQUEST)

        guide_serializer = self.get_serializer(data=request.data)
        guide_serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                guide = guide_serializer.save()

                for key, uploaded_file in request.FILES.items():
                    if key.startswith('files[') and key.endswith(']'):
                        doc_type_id = key[6:-1]
                        try:
                            doc_type = DocumentType.objects.get(id=doc_type_id)
                            Document.objects.create(
                                clinic=clinic,
                                content_object=guide,
                                type=doc_type,
                                file=uploaded_file,
                                created_by=request.user
                            )
                        except DocumentType.DoesNotExist:
                            pass
            
            headers = self.get_success_headers(guide_serializer.data)
            return Response(guide_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
