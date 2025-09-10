from rest_framework import serializers
from .models import Document, DocumentType
from django.contrib.contenttypes.models import ContentType
from audit.mixins import AuditableSerializerMixin

class DocumentTypeSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'category']

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    type = DocumentTypeSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'type', 'description', 'file', 'file_url', 'created_at', 'clinic']

    def get_file_url(self, obj):
        return obj.file.url

class DocumentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating documents in a nested context."""
    description = serializers.CharField(required=False, allow_blank=True)
    type = serializers.PrimaryKeyRelatedField(queryset=DocumentType.objects.all())

    class Meta:
        model = Document
        fields = ['file', 'type', 'description']


class DocumentUploadSerializer(serializers.ModelSerializer):
    content_type_str = serializers.CharField(write_only=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Document
        fields = ['file', 'type', 'description', 'object_id', 'content_type_str', 'clinic']

    def validate(self, data):
        try:
            app_label, model = data['content_type_str'].split('.')
            data['content_type'] = ContentType.objects.get(app_label=app_label, model=model)
        except (ContentType.DoesNotExist, ValueError):
            raise serializers.ValidationError("Invalid content_type_str.")
        del data['content_type_str']
        return data