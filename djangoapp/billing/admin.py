from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from .models import Payer, Guide
from documents.models import Document
from documents.admin import DocumentInline
from audit.models import AuditDecision

@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'payer_type', 'is_active')
    list_filter = ('payer_type', 'is_active', 'clinics')
    search_fields = ('name',)
    filter_horizontal = ('clinics',)

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'clinic',
        'guide_type',
        'status',
        'payer',
        'authorization_number',
    )
    list_filter = (
        'status',
        'guide_type',
        'clinic',
        'payer',
    )
    search_fields = (
        'patient__full_name',
        'patient__cpf',
        'authorization_number',
    )
    readonly_fields = ('clinic',)
    autocomplete_fields = ('patient', 'payer')

    fieldsets = (
        (_('Informações Gerais'), {
            'fields': ('patient', 'clinic', 'payer', 'guide_type', 'nature', 'status')
        }),
        (_('Detalhes da Autorização'), {
            'fields': ('authorization_number', 'valid_from', 'valid_to')
        }),
    )

    inlines = [DocumentInline]
    actions = ['mark_as_approved', 'mark_as_rejected']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Document) and not instance.pk:
                instance.created_by = request.user
                if hasattr(form.instance, 'patient') and hasattr(form.instance.patient, 'clinic'):
                    instance.clinic = form.instance.patient.clinic
                instance.save()
        super().save_formset(request, form, formset, change)
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