from django.contrib import admin
from .models import AuditDecision

@admin.register(AuditDecision)
class AuditDecisionAdmin(admin.ModelAdmin):
    list_display = ('guide', 'decision', 'auditor', 'audited_at')
    list_filter = ('decision', 'auditor', 'audited_at')
    # Torna o admin inteiro read-only, pois uma decisão não deve ser alterada.
    readonly_fields = [f.name for f in AuditDecision._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False