from rest_framework import serializers
from .models import Document, DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name']

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    type = DocumentTypeSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'type', 'file', 'file_url', 'created_at']

    def get_file_url(self, obj):
        return obj.file.url
