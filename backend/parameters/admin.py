
from django.contrib import admin
from .models import ParameterRule

@admin.register(ParameterRule)
class ParameterRuleAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'context',
        'is_active',
    )
    list_filter = (
        'is_active',
        'context',
        'payer',
        'guide_type',
        'nature',
    )
    search_fields = (
        'payer__name',
    )
    
    fieldsets = (
        ('Condições da Regra', {
            'fields': ('is_active', 'payer', 'context')
        }),
        ('Critérios (Apenas para Guias)', {
            'classes': ('collapse',),
            'description': 'Preencha apenas se o contexto for "Guia de Faturamento".',
            'fields': ('guide_type', 'nature')
        }),
        ('Documentos Obrigatórios', {
            'fields': ('required_documents',)
        }),
    )

    filter_horizontal = ('required_documents',)