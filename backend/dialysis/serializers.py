from rest_framework import serializers
from .models import Patient, PatientHistory, ExitType
from organization.models import Clinic
from documents.serializers import DocumentSerializer

class ExitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExitType
        fields = ['id', 'name', 'code', 'clinics']

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name']

class PatientSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    clinic_id = serializers.PrimaryKeyRelatedField(
        queryset=Clinic.objects.all(), source='clinic', write_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'cpf', 'cns', 
            'clinic', 'clinic_id', 'status', 'patient_type',
            'documents'
        ]

class PatientHistorySerializer(serializers.ModelSerializer):
    exit_type = ExitTypeSerializer(read_only=True)
    exit_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ExitType.objects.all(), source='exit_type', write_only=True, allow_null=True
    )

    class Meta:
        model = PatientHistory
        fields = '__all__'