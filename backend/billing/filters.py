import django_filters
from .models import Guide

class GuideFilter(django_filters.FilterSet):
    class Meta:
        model = Guide
        fields = {
            'patient__full_name': ['icontains'],
            'clinic': ['exact'],
            'payer': ['exact'],
            'guide_type': ['exact'],
            'status': ['exact'],
            'nature': ['exact'],
            'valid_from': ['gte', 'lte'],
            'valid_to': ['gte', 'lte'],
        }
