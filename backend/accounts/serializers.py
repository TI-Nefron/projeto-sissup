from rest_framework import serializers
from .models import CustomUser
from organization.models import Clinic
from organization.serializers import ClinicSerializer

class UserSerializer(serializers.ModelSerializer):
    clinics = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'clinics')

    def get_clinics(self, obj):
        if obj.is_superuser:
            queryset = Clinic.objects.all()
        else:
            queryset = obj.clinics.all()
        return ClinicSerializer(queryset, many=True).data
