from rest_framework import serializers
from .models import GuideType, ProcedureStatus, ParameterRule
from audit.mixins import AuditableSerializerMixin

class GuideTypeSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = GuideType
        fields = ['id', 'name', 'is_active', 'clinics']

class ProcedureStatusSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ProcedureStatus
        fields = ['id', 'name', 'slug', 'is_active', 'clinics']

class ParameterRuleSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ParameterRule
        fields = '__all__'
