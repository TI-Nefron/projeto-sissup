from rest_framework import serializers
from .models import Patient, PatientHistory, ExitType
from organization.models import Clinic
from documents.serializers import DocumentSerializer, DocumentCreateSerializer
from documents.models import Document, DocumentType
from django.db import transaction
from audit.mixins import AuditableSerializerMixin

class ExitTypeSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ExitType
        fields = ['id', 'name', 'code', 'clinics']

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name']

class PatientSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    clinic_id = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(), source='clinic', write_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)
    documents_data = serializers.ListField(
        child=DocumentCreateSerializer(), write_only=True, required=False
    )

    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'cpf', 'cns', 
            'clinic', 'clinic_id', 'status', 'patient_type',
            'documents', 'documents_data'
        ]

    def validate(self, data):
        # On creation, check for mandatory documents
        if not self.instance:
            clinic = data.get('clinic')
            if clinic:
                mandatory_docs = clinic.mandatory_document_types.filter(category=DocumentType.Category.PATIENT)
                provided_doc_types = {doc['type'] for doc in data.get('documents_data', [])}
                
                missing_docs = []
                for mandatory_doc in mandatory_docs:
                    if mandatory_doc not in provided_doc_types:
                        missing_docs.append(mandatory_doc.name)
                
                if missing_docs:
                    raise serializers.ValidationError({
                        "documents_data": f"Documentos obrigatórios faltando: {', '.join(missing_docs)}"
                    })
        return data

    def _create_documents(self, patient, documents_data):
        user = self.context['request'].user
        for doc_data in documents_data:
            Document.objects.create(
                clinic=patient.clinic,
                content_object=patient,
                created_by=user,
                **doc_data
            )

    @transaction.atomic
    def create(self, validated_data):
        documents_data = validated_data.pop('documents_data', [])
        patient = super().create(validated_data)
        self._create_documents(patient, documents_data)
        return patient

    @transaction.atomic
    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents_data', [])
        patient = super().update(instance, validated_data)
        self._create_documents(patient, documents_data)
        return patient

class PatientHistorySerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    exit_type = ExitTypeSerializer(read_only=True)
    exit_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ExitType.objects.all(), source='exit_type', write_only=True, allow_null=True
    )

    class Meta:
        model = PatientHistory
        fields = '__all__'