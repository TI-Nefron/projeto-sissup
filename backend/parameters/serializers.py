from rest_framework import serializers
from .models import GuideType, ProcedureStatus

class GuideTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideType
        fields = ['id', 'name', 'is_active', 'clinics']

class ProcedureStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureStatus
        fields = ['id', 'name', 'slug', 'is_active', 'clinics']
