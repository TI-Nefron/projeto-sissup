from rest_framework import serializers
from .models import Clinic
from audit.mixins import AuditableSerializerMixin

class ClinicSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'
