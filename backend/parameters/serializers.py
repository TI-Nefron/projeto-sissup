from rest_framework import serializers
from .models import GuideType, ProcedureStatus

class GuideTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideType
        fields = ['id', 'name']

class ProcedureStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureStatus
        fields = ['id', 'name', 'slug']
