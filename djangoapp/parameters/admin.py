from django.contrib import admin
from .models import ParameterRule

@admin.register(ParameterRule)
class ParameterRuleAdmin(admin.ModelAdmin):
    list_display = ('payer', 'guide_type', 'nature', 'document_type', 'is_mandatory')
    list_filter = ('payer', 'guide_type', 'nature')