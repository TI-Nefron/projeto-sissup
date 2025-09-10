from rest_framework import serializers
from django.contrib.auth import get_user_model
from organization.models import Clinic
from parameters.models import GuideType, ProcedureStatus
from dialysis.models import ExitType
from accounts.models import Role, Permission
from audit.mixins import AuditableSerializerMixin

User = get_user_model()

class PermissionSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'clinics', 'roles', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        user = User.objects.create_user(**validated_data)
        user.roles.set(roles)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        roles = validated_data.pop('roles', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        if roles is not None:
            user.roles.set(roles)

        return user

class ClinicSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class GuideTypeSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = GuideType
        fields = '__all__'

class ProcedureStatusSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ProcedureStatus
        fields = '__all__'

class ExitTypeSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ExitType
        fields = '__all__'
