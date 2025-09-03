from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from .models import Payer, Guide
from documents.models import Document
from documents.admin import DocumentInline
from audit.models import AuditDecision

@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'guide_type',
        'status',
        'payer',
        'authorization_number',
        'created_at'
    )
    list_filter = (
        'status',
        'guide_type',
        'nature',
        'patient__clinic',
        'payer'
    )
    search_fields = (
        'patient__full_name',
        'patient__cpf',
        'authorization_number'
    )
    autocomplete_fields = ('patient', 'payer')

    fieldsets = (
        (_('Informações Gerais'), {
            'fields': ('patient', 'payer', 'guide_type', 'nature', 'status')
        }),
        (_('Detalhes da Autorização'), {
            'fields': ('authorization_number', 'valid_from', 'valid_to')
        }),
    )

    inlines = [DocumentInline]
    actions = ['mark_as_approved', 'mark_as_rejected']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if hasattr(formset, 'new_objects'):
                instances = formset.save(commit=False)
                for instance in instances:
                    if isinstance(instance, Document) and not instance.pk:
                        instance.created_by = request.user
                        if hasattr(form.instance, 'patient') and hasattr(form.instance.patient, 'clinic'):
                            instance.clinic = form.instance.patient.clinic
                        instance.save()
                formset.save_m2m()

    @admin.action(description=_("Marcar selecionadas como APROVADO PELA AUDITORIA"))
    def mark_as_approved(self, request, queryset):
        updated_count = 0
        for guide in queryset:
            guide.status = Guide.Status.APPROVED
            guide.save()
            AuditDecision.objects.create(
                guide=guide,
                decision=AuditDecision.Decision.APPROVED,
                auditor=request.user,
                comments=_("Aprovado via ação em massa no admin.")
            )
            updated_count += 1
        self.message_user(
            request,
            f"{updated_count} guia(s) foram aprovadas com sucesso.",
            messages.SUCCESS
        )

    @admin.action(description=_("Marcar selecionadas como RECUSADO COM PENDÊNCIA"))
    def mark_as_rejected(self, request, queryset):
        updated_count = 0
        for guide in queryset:
            guide.status = Guide.Status.IN_REVIEW
            guide.save()
            AuditDecision.objects.create(
                guide=guide,
                decision=AuditDecision.Decision.REJECTED,
                auditor=request.user,
                comments=_("Recusado via ação em massa no admin. Verifique as pendências.")
            )
            updated_count += 1
        self.message_user(
            request,
            f"{updated_count} guia(s) foram marcadas com pendência.",
            messages.WARNING
        )