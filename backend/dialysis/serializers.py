from rest_framework import serializers
from .models import Patient
from organization.models import Clinic

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name']

class PatientSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'cpf', 'cns', 
            'clinic', 'status', 'patient_type'
        ]