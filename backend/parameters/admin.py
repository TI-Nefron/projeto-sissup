from django.contrib import admin
from .models import ParameterRule, GuideType, ProcedureStatus

@admin.register(GuideType)
class GuideTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(ProcedureStatus)
class ProcedureStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

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
        ('Critérios (Apenas para Guias de Faturamento)', {
            'classes': ('collapse',),
            'description': 'Estes campos são aplicáveis apenas quando o contexto é "Guia de Faturamento".',
            'fields': ('guide_type', 'nature')
        }),
        ('Documentos Obrigatórios', {
            'fields': ('required_documents',)
        }),
    )

    filter_horizontal = ('required_documents',)