from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from .serializers import AuditLogSerializer
from .filters import AuditLogFilter
from django_filters.rest_framework import DjangoFilterBackend

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuditLogFilter

class ContentTypeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        app_label = request.query_params.get('app_label')
        model = request.query_params.get('model')
        if not app_label or not model:
            return Response({'error': 'app_label and model parameters are required.'}, status=400)
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            return Response({'id': content_type.id, 'app_label': content_type.app_label, 'model': content_type.model})
        except ContentType.DoesNotExist:
            return Response({'error': 'ContentType not found.'}, status=404)
