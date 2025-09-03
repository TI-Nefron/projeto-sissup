
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Document
from .constants import PatientDocumentType, GuideDocumentType
from billing.models import Guide
from dialysis.models import Patient

class DocumentInline(GenericTabularInline):
    model = Document
    fields = ('type', 'file', 'created_at', 'sha256')
    readonly_fields = ('created_at', 'sha256')
    extra = 1
    exclude = ('clinic', 'created_by')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        if isinstance(obj, Guide):
            choices = GuideDocumentType.choices
        elif isinstance(obj, Patient):
            choices = PatientDocumentType.choices
        else:
            choices = []
        
        formset.form.base_fields['type'].choices = choices
        return formset

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'content_object',
        'clinic',
        'type',
        'created_at',
        'created_by'
    )
    list_filter = (
        'clinic',
        'type',
        'content_type'
    )
    
    readonly_fields = [
        field.name for field in Document._meta.fields
    ]
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False