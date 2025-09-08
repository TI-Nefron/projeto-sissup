from rest_framework import serializers
from .models import Guide, Payer
from dialysis.models import Patient
from organization.models import Clinic
from parameters.models import GuideType, ProcedureStatus
from documents.serializers import DocumentSerializer

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

class GuideTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideType
        fields = ['id', 'name']

class ProcedureStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureStatus
        fields = ['id', 'name', 'slug']

class GuideSerializer(serializers.ModelSerializer):
    patient = PatientNameSerializer(read_only=True)
    clinic = ClinicNameSerializer(read_only=True)
    payer = PayerNameSerializer(read_only=True)
    guide_type = GuideTypeSerializer(read_only=True)
    status = ProcedureStatusSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = [
            'id', 'patient', 'clinic', 'payer', 'guide_type', 'nature',
            'authorization_number', 'status', 'valid_from', 'valid_to',
            'created_at', 'updated_at', 'documents'
        ]
