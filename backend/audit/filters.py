from django_filters import rest_framework as filters
from .models import AuditLog

class AuditLogFilter(filters.FilterSet):
    class Meta:
        model = AuditLog
        fields = {
            'content_type': ['exact'],
            'object_id': ['exact'],
        }
