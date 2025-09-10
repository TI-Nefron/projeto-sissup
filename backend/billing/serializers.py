from rest_framework import serializers
from .models import Guide, Payer
from dialysis.models import Patient
from organization.models import Clinic
from parameters.models import GuideType, ProcedureStatus, ParameterRule
from documents.serializers import DocumentSerializer, DocumentCreateSerializer
from documents.models import Document
from django.db import transaction
from audit.mixins import AuditableSerializerMixin

class PatientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name']

class ClinicNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name']

class PayerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = ['id', 'name']

class PayerSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = ['id', 'name', 'payer_type', 'is_active', 'clinics']

class GuideTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideType
        fields = ['id', 'name']

class ProcedureStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureStatus
        fields = ['id', 'name', 'slug']

class GuideSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    clinic = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all(), required=False)
    payer = serializers.PrimaryKeyRelatedField(queryset=Payer.objects.all())
    guide_type = serializers.PrimaryKeyRelatedField(queryset=GuideType.objects.all())
    status = ProcedureStatusSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    documents_data = serializers.ListField(
        child=DocumentCreateSerializer(), write_only=True, required=False
    )

    class Meta:
        model = Guide
        fields = [
            'id', 'patient', 'clinic', 'payer', 'guide_type', 'nature',
            'authorization_number', 'status', 'valid_from', 'valid_to',
            'created_at', 'updated_at', 'documents', 'documents_data'
        ]

    def validate(self, data):
        if not self.instance: # Only on create
            payer = data.get('payer')
            guide_type = data.get('guide_type')
            nature = data.get('nature')

            if payer and guide_type and nature:
                rules = ParameterRule.objects.filter(
                    payer=payer,
                    guide_type=guide_type,
                    nature=nature,
                    is_active=True
                )
                if rules.exists():
                    rule = rules.first()
                    mandatory_docs = rule.required_documents.all()
                    provided_doc_types = {doc['type'] for doc in data.get('documents_data', [])}

                    missing_docs = []
                    for mandatory_doc in mandatory_docs:
                        if mandatory_doc not in provided_doc_types:
                            missing_docs.append(mandatory_doc.name)
                    
                    if missing_docs:
                        raise serializers.ValidationError({
                            "documents_data": f"Documentos obrigatórios faltando para esta combinação de convênio, tipo de guia e natureza: {', '.join(missing_docs)}"
                        })
        return data

    def _create_documents(self, guide, documents_data):
        user = self.context['request'].user
        for doc_data in documents_data:
            Document.objects.create(
                clinic=guide.clinic,
                content_object=guide,
                created_by=user,
                **doc_data
            )

    @transaction.atomic
    def create(self, validated_data):
        documents_data = validated_data.pop('documents_data', [])
        guide = super().create(validated_data)
        self._create_documents(guide, documents_data)
        return guide

    @transaction.atomic
    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents_data', [])
        guide = super().update(instance, validated_data)
        self._create_documents(guide, documents_data)
        return guide