from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .serializers import DocumentUploadSerializer, DocumentTypeSerializer
from .models import DocumentType
from audit.mixins import AuditableViewSetMixin
from audit.models import AuditLog, log_change

class DocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(created_by=request.user)
            log_change(
                user=request.user,
                instance=document,
                action=AuditLog.Action.CREATE,
                changes={'state': serializer.data}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentTypeViewSet(AuditableViewSetMixin, viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAdminUser]
