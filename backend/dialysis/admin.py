from django.contrib import admin
from .models import Patient
from documents.models import Document
from documents.admin import DocumentInline

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'clinic',
        'status',
        'is_active',
        'patient_type',
        'cpf',
        'payer',
    )
    list_filter = (
        'is_active',
        'clinic',
        'status',
        'patient_type',
        'payer',
    )
    search_fields = (
        'full_name',
        'cpf',
        'cns',
    )
    ordering = ('full_name',)

    fieldsets = (
        ('Associação Institucional', {
            'fields': ('clinic', 'payer')
        }),
        ('Identificação Pessoal', {
            'fields': ('full_name', 'cpf', 'cns')
        }),
        ('Informações Clínicas', {
            'fields': ('patient_type', 'cid_principal', 'status', 'is_active')
        }),
    )
    
    inlines = [DocumentInline]

    def save_formset(self, request, form, formset, change):
        form.instance.save()
        for instance in formset.save(commit=False):
            instance.created_by = request.user
            instance.clinic = form.instance.clinic
            instance.save()